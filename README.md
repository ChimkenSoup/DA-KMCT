# DA-KMCT: Density-Aware k-Means Clustering of Trajectories

A from-scratch Python implementation of the **DA-KMCT** algorithm from the research paper:

> **"KMCT: k-Means Clustering of Trajectories Efficiently in Location-Based Services"**
> Liu et al., 2024
> Reference implementation: [yuanjun-liu/KMCT](https://github.com/yuanjun-liu/KMCT)

---

## Overview

Standard k-means cannot handle **trajectory data** (sequences of GPS waypoints) for two reasons:

1. **Variable-length trajectories** — paths recorded at different sampling rates have different numbers of points, making naive Euclidean comparison meaningless.
2. **Saddle-point convergence** — random centroid initialisation in high-dimensional trajectory space frequently gets stuck at poor local minima.

DA-KMCT solves both problems:

| Problem | Solution |
|---|---|
| Variable lengths | **ITS semantic interpolation** — resamples every trajectory to `h` arc-length-uniform waypoints |
| Saddle points | **Density-aware initialisation + weighted M-step** — seeds centroids at density peaks and weights updates by local trajectory density |

---

## Algorithm Pipeline

```
Tabular data
    │
    ▼
[1] Build Trajectories
    Map features → spatial waypoints (e.g., Iris 4 features → 2-step 2D trajectory)
    │
    ▼
[2] ITS Semantic Interpolation
    Resample every trajectory to h uniformly arc-length-spaced points
    Arc-length spacing:  e = L(T) / (h − 1)
    │
    ▼
[3] Build Density Map
    Quantise the [0,1]² feature space into a grid_cells × grid_cells grid
    Count waypoints per cell → normalised density histogram
    │
    ▼
[4] Density-Based Initialisation
    Seed k centroids at the k densest grid cells (avoids saddle points)
    │
    ▼
[5] EM Loop (until convergence)
    E-step: assign each trajectory to nearest centroid (Euclidean in ITS space)
    M-step: update centroids using density-weighted mean
            centroid_c = Σ w(T)·v(T) / Σ w(T)
            where w(T) = mean density over trajectory's waypoints
    │
    ▼
[6] Output: cluster labels + centroids
```

---

## Dataset

The demo uses the **Iris dataset** (150 samples, 4 features), transformed into trajectories as follows:

```
[sepal_length, sepal_width, petal_length, petal_width]
       ↓                           ↓
 waypoint_0 = (x₀, y₀)     waypoint_1 = (x₁, y₁)
```

All features are min-max normalised to `[0, 1]` before processing. ITS then resamples each 2-waypoint trajectory to `h = 5` uniformly spaced points.

---

## Results (Iris, k=3)

| Metric | Value |
|---|---|
| Execution time | **~0.09 seconds** |
| EM iterations | 15 (converged early, max=300) |
| Inertia (SSE) | 15.69 |
| Cluster purity | **0.88** (88%) |
| Cluster sizes | {0: 48, 1: 50, 2: 52} |

### Final Cluster Centroids (ITS waypoints, normalised [0,1])

| Cluster | Dominant Species | wp0 | wp1 | wp2 | wp3 | wp4 |
|---|---|---|---|---|---|---|
| 0 | versicolor | (0.43, 0.30) | (0.47, 0.36) | (0.50, 0.41) | (0.53, 0.47) | (0.57, 0.53) |
| 1 | setosa     | (0.19, 0.58) | (0.16, 0.45) | (0.13, 0.32) | (0.11, 0.19) | (0.08, 0.06) |
| 2 | virginica  | (0.62, 0.44) | (0.64, 0.52) | (0.67, 0.60) | (0.69, 0.67) | (0.72, 0.75) |

---

## Installation

```bash
pip install numpy pandas scikit-learn
```

> **Note:** `scikit-learn` is used **only** to load the Iris dataset. All clustering logic is implemented from scratch — `sklearn.cluster.KMeans` is never imported.

---

## Usage

```bash
python da_kmct_implementation.py
```

Or import the class directly:

```python
from da_kmct_implementation import DA_KMCT, its_transform, build_trajectories_from_iris

# Build trajectories
trajectories, ground_truth = build_trajectories_from_iris()

# ITS normalisation
resampled, h = its_transform(trajectories)

# Fit DA-KMCT
model = DA_KMCT(k=3, grid_cells=10, max_iter=300, tol=5e-3, random_state=42)
model.fit(resampled, h)

print("Labels:", model.labels_)
print("Centroids shape:", model.centroids_.shape)  # (3, h*2)
```

---

## Key Classes & Functions

| Name | Description |
|---|---|
| `build_trajectories_from_iris()` | Load Iris + transform to 2-step 2D trajectories |
| `trajectory_arc_length(T)` | Compute total polyline length L(T) |
| `interpolate_trajectory(T, h)` | ITS resampling to h uniform arc-length points |
| `its_transform(trajectories)` | Apply ITS to a full list of trajectories |
| `DA_KMCT` | Main clustering class |
| `DA_KMCT._build_density_map()` | 2D histogram of waypoint counts per grid cell |
| `DA_KMCT._density_init()` | Density-peak-based centroid initialisation |
| `DA_KMCT._density_weight()` | Per-trajectory density weight w(T) |
| `DA_KMCT.fit()` | Full EM loop with density-weighted M-step |
| `DA_KMCT.predict()` | Assign new trajectories to fitted clusters |
| `purity_score()` | Evaluate clustering quality vs ground truth |

---

## File Structure

```
DA-KMCT/
├── da_kmct_implementation.py   # Full implementation (~550 lines, heavily documented)
├── DAKMCT.pdf                  # Original paper (Liu et al., 2024)
└── README.md                   # This file
```

---

## References

- Liu, Y. et al. (2024). *KMCT: k-Means Clustering of Trajectories Efficiently in Location-Based Services.*
- Reference implementation: https://github.com/yuanjun-liu/KMCT
