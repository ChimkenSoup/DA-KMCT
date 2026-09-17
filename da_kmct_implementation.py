import numpy as np
import time
from typing import List, Tuple, Optional
from sklearn.datasets import load_iris
import pandas as pd

def build_trajectories_from_iris() -> Tuple[List[np.ndarray], np.ndarray]:
    iris = load_iris()
    X = iris.data.astype(float)
    y = iris.target
    col_min = X.min(axis=0)
    col_max = X.max(axis=0)
    X_norm = (X - col_min) / (col_max - col_min + 1e-12)
    trajectories: List[np.ndarray] = []
    for i in range(len(X_norm)):
        wp0 = X_norm[i, :2]
        wp1 = X_norm[i, 2:]
        T = np.array([wp0, wp1])
        trajectories.append(T)
    return (trajectories, y)

def trajectory_arc_length(T: np.ndarray) -> float:
    length = 0.0
    for i in range(len(T) - 1):
        segment_len = np.linalg.norm(T[i, :2] - T[i + 1, :2])
        length += segment_len
    return length

def interpolate_trajectory(T: np.ndarray, h: int) -> np.ndarray:
    L = trajectory_arc_length(T)
    vec = np.array([T[0].copy() for _ in range(h)])
    vec[-1] = T[-1].copy()
    if L < 1e-12:
        return vec
    e = L / (h - 1)
    accumulated_arc = 0.0
    next_output_arc = 0.0
    j = 0
    for i in range(1, len(T)):
        p_prev = T[i - 1]
        p_curr = T[i]
        seg_len = np.linalg.norm(p_prev[:2] - p_curr[:2])
        if seg_len < 1e-12:
            continue
        accumulated_arc += seg_len
        while accumulated_arc >= next_output_arc:
            if j >= h:
                break
            dist_back = accumulated_arc - next_output_arc
            frac = dist_back / seg_len
            vec[j] = p_curr + frac * (p_prev - p_curr)
            j += 1
            next_output_arc += e
    return vec

def its_transform(trajectories: List[np.ndarray]) -> Tuple[List[np.ndarray], int]:
    mean_len = int(np.mean([len(T) for T in trajectories]))
    h = max(mean_len, 5)
    resampled = [interpolate_trajectory(T, h)[:, :2] for T in trajectories]
    return (resampled, h)

class DA_KMCT:

    def __init__(self, k: int=3, grid_cells: int=10, max_iter: int=300, tol: float=0.005, random_state: Optional[int]=42):
        self.k = k
        self.grid_cells = grid_cells
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids_: Optional[np.ndarray] = None
        self.labels_: Optional[np.ndarray] = None
        self.density_map_: Optional[np.ndarray] = None
        self.n_iter_: int = 0
        self.inertia_: float = float('inf')
        self._rng = np.random.default_rng(random_state)

    def _build_density_map(self, vectors: np.ndarray, h: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        n = len(vectors)
        g = self.grid_cells
        all_points = vectors.reshape(n * h, 2)
        xs = all_points[:, 0]
        ys = all_points[:, 1]
        density_map, x_edges, y_edges = np.histogram2d(xs, ys, bins=g, range=[[0.0, 1.0], [0.0, 1.0]])
        total = density_map.sum()
        if total > 0:
            density_map /= total
        return (density_map, x_edges, y_edges)

    def _density_init(self, vectors: np.ndarray, density_map: np.ndarray, x_edges: np.ndarray, y_edges: np.ndarray, h: int) -> np.ndarray:
        g = self.grid_cells
        n = len(vectors)
        flat_density = density_map.flatten()
        sorted_cell_ids = np.argsort(flat_density)[::-1]
        first_wps = vectors[:, :2]
        centroids = []
        used_cell_ids = set()
        for cell_id in sorted_cell_ids:
            if len(centroids) >= self.k:
                break
            if cell_id in used_cell_ids:
                continue
            row = cell_id // g
            col = cell_id % g
            x_lo, x_hi = (x_edges[row], x_edges[row + 1])
            y_lo, y_hi = (y_edges[col], y_edges[col + 1])
            in_cell = (first_wps[:, 0] >= x_lo) & (first_wps[:, 0] <= x_hi) & (first_wps[:, 1] >= y_lo) & (first_wps[:, 1] <= y_hi)
            indices_in_cell = np.where(in_cell)[0]
            if len(indices_in_cell) == 0:
                continue
            centroid = vectors[indices_in_cell].mean(axis=0)
            centroids.append(centroid)
            used_cell_ids.add(cell_id)
        if len(centroids) < self.k:
            already_used = set()
            for c in centroids:
                dists = np.linalg.norm(vectors - c, axis=1)
                already_used.add(int(np.argmin(dists)))
            remaining = list(set(range(n)) - already_used)
            if remaining:
                extras = self._rng.choice(remaining, size=min(self.k - len(centroids), len(remaining)), replace=False)
                for idx in extras:
                    centroids.append(vectors[idx].copy())
        while len(centroids) < self.k:
            idx = int(self._rng.integers(0, n))
            centroids.append(vectors[idx].copy())
        return np.array(centroids[:self.k])

    @staticmethod
    def _trajectory_distance(v1: np.ndarray, v2: np.ndarray) -> float:
        return float(np.linalg.norm(v1 - v2))

    def _density_weight(self, vector: np.ndarray, density_map: np.ndarray, x_edges: np.ndarray, y_edges: np.ndarray, h: int) -> float:
        g = self.grid_cells
        waypoints = vector.reshape(h, 2)
        weight = 0.0
        for wp in waypoints:
            x, y = (wp[0], wp[1])
            row = min(int(np.searchsorted(x_edges, x, side='right')) - 1, g - 1)
            col = min(int(np.searchsorted(y_edges, y, side='right')) - 1, g - 1)
            row = max(row, 0)
            col = max(col, 0)
            weight += density_map[row, col]
        weight /= h
        return weight

    def _has_converged(self, old_centroids: np.ndarray, new_centroids: np.ndarray) -> bool:
        max_displacement = max((np.linalg.norm(new_centroids[c] - old_centroids[c]) for c in range(self.k)))
        return max_displacement < self.tol

    def fit(self, resampled_trajectories: List[np.ndarray], h: int) -> 'DA_KMCT':
        n = len(resampled_trajectories)
        vectors = np.array([T.flatten() for T in resampled_trajectories])
        density_map, x_edges, y_edges = self._build_density_map(vectors, h)
        self.density_map_ = density_map
        centroids = self._density_init(vectors, density_map, x_edges, y_edges, h)
        labels = np.zeros(n, dtype=int)
        for epoch in range(self.max_iter):
            old_centroids = centroids.copy()
            for i in range(n):
                distances = [self._trajectory_distance(vectors[i], centroids[c]) for c in range(self.k)]
                labels[i] = int(np.argmin(distances))
            new_centroids = np.zeros_like(centroids)
            for c in range(self.k):
                cluster_mask = labels == c
                cluster_indices = np.where(cluster_mask)[0]
                if len(cluster_indices) == 0:
                    new_centroids[c] = vectors[int(self._rng.integers(0, n))].copy()
                    continue
                weights = np.array([self._density_weight(vectors[idx], density_map, x_edges, y_edges, h) for idx in cluster_indices])
                weight_sum = weights.sum()
                cluster_vectors = vectors[cluster_indices]
                if weight_sum < 1e-15:
                    new_centroids[c] = cluster_vectors.mean(axis=0)
                else:
                    weighted_vecs = weights[:, np.newaxis] * cluster_vectors
                    new_centroids[c] = weighted_vecs.sum(axis=0) / weight_sum
            centroids = new_centroids
            self.n_iter_ = epoch + 1
            if self._has_converged(old_centroids, centroids):
                break
        self.centroids_ = centroids
        self.labels_ = labels
        self.inertia_ = sum((self._trajectory_distance(vectors[i], centroids[labels[i]]) ** 2 for i in range(n)))
        return self

    def predict(self, resampled_trajectories: List[np.ndarray]) -> np.ndarray:
        if self.centroids_ is None:
            raise RuntimeError('Call fit() before predict().')
        vectors = np.array([T.flatten() for T in resampled_trajectories])
        labels = np.zeros(len(vectors), dtype=int)
        for i in range(len(vectors)):
            distances = [self._trajectory_distance(vectors[i], self.centroids_[c]) for c in range(self.k)]
            labels[i] = int(np.argmin(distances))
        return labels

    def centroid_waypoints(self, h: int) -> List[np.ndarray]:
        if self.centroids_ is None:
            raise RuntimeError('Call fit() first.')
        return [self.centroids_[c].reshape(h, 2) for c in range(self.k)]

def purity_score(labels: np.ndarray, ground_truth: np.ndarray) -> float:
    n = len(labels)
    total_correct = 0
    for c in np.unique(labels):
        mask = labels == c
        gt_in_cluster = ground_truth[mask]
        if len(gt_in_cluster) == 0:
            continue
        unique_classes, counts = np.unique(gt_in_cluster, return_counts=True)
        total_correct += counts.max()
    return total_correct / n

def print_centroid_table(model: 'DA_KMCT', h: int) -> None:
    centroid_wps = model.centroid_waypoints(h)
    rows = []
    for c, wp_array in enumerate(centroid_wps):
        row = {'Cluster': c}
        for step in range(h):
            row[f'wp{step}_x'] = round(wp_array[step, 0], 4)
            row[f'wp{step}_y'] = round(wp_array[step, 1], 4)
        rows.append(row)
    df = pd.DataFrame(rows).set_index('Cluster')
    print('\n' + '=' * 60)
    print('  FINAL CLUSTER CENTROIDS  (ITS waypoints, normalised [0,1])')
    print('=' * 60)
    print(df.to_string())
    print('=' * 60 + '\n')
if __name__ == '__main__':
    print()
    print('+' + '-' * 68 + '+')
    print('|   DA-KMCT: Density-Aware k-Means Clustering of Trajectories    |')
    print('|   Dataset : Iris (150 samples -> 2-step 2-D trajectories)      |')
    print('+' + '-' * 68 + '+')
    print()
    t_start = time.perf_counter()
    print('>> Step A - Loading Iris dataset and building trajectories...')
    trajectories, ground_truth = build_trajectories_from_iris()
    print(f'   * {len(trajectories)} trajectories created (2 waypoints x 2 dims each).')
    print(f'   * Sample trajectory[0]: wp0={trajectories[0][0]}, wp1={trajectories[0][1]}')
    print('\n>> Step B - Applying ITS (Semantic Interpolation) normalisation...')
    resampled, h = its_transform(trajectories)
    print(f'   * Target h = {h} waypoints per trajectory (clipped to min 5).')
    print(f'   * Resampled trajectory[0] shape: {resampled[0].shape}')
    print(f'   * Resampled trajectory[0] waypoints:')
    for step_idx, wp in enumerate(resampled[0]):
        print(f'     wp{step_idx}: ({wp[0]:.4f}, {wp[1]:.4f})')
    print('\n>> Step C - Running DA-KMCT (k=3, grid_cells=10, max_iter=300)...')
    model = DA_KMCT(k=3, grid_cells=10, max_iter=300, tol=0.005, random_state=42)
    model.fit(resampled, h)
    t_end = time.perf_counter()
    execution_time = t_end - t_start
    print(f"\n{'=' * 68}")
    print('  RESULTS')
    print(f"{'=' * 68}")
    print(f'  Iterations run        : {model.n_iter_}  (max={model.max_iter})')
    print(f'  Inertia (SSE)         : {model.inertia_:.4f}')
    print(f'  Execution time        : {execution_time:.4f} seconds')
    print(f"{'-' * 68}")
    unique_labels, counts = np.unique(model.labels_, return_counts=True)
    print('  Cluster sizes         :', dict(zip(unique_labels.tolist(), counts.tolist())))
    purity = purity_score(model.labels_, ground_truth)
    print(f'  Clustering purity     : {purity:.4f}  (1.0 = perfect, 0.33 = random)')
    print(f"{'=' * 68}")
    print_centroid_table(model, h)
    print('>> Final centroid waypoints (in normalised feature space):')
    centroid_wps = model.centroid_waypoints(h)
    species_names = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    for c, wps in enumerate(centroid_wps):
        cluster_species = ground_truth[model.labels_ == c]
        majority_class = int(np.bincount(cluster_species).argmax())
        print(f'\n   Cluster {c}  (dominant Iris species: {species_names[majority_class]})')
        for step in range(h):
            print(f'     Waypoint {step}: ({wps[step, 0]:.4f}, {wps[step, 1]:.4f})')
    print('\n>> First 20 sample labels (predicted vs ground-truth):')
    print(f"  {'Sample':>6}  {'Predicted':>9}  {'True':>4}  {'Match':>5}")
    print('  ' + '-' * 33)
    for i in range(20):
        match = 'YES' if model.labels_[i] == ground_truth[i] else '---'
        print(f'  {i:>6}  {model.labels_[i]:>9}  {ground_truth[i]:>4}  {match:>5}')
    print(f'\n  [Note: cluster IDs vs class IDs may differ by permutation;')
    print(f'   use purity_score above for cluster quality measurement.]\n')
    print(f'DA-KMCT complete in {execution_time:.4f} seconds.\n')
