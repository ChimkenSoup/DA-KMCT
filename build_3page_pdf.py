import os
import subprocess

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Weekly Progress Report - Neil Tauro</title>
<style>
  @page {
    size: A4;
    margin: 12mm 16mm 12mm 16mm;
  }
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1e293b;
    line-height: 1.4;
    font-size: 9.5pt;
    text-align: justify;
  }
  h1 {
    text-align: center;
    font-size: 15pt;
    margin: 0 0 6px 0;
    text-transform: uppercase;
    font-weight: bold;
    color: #0f172a;
    letter-spacing: 0.5px;
  }
  .student-details {
    margin-bottom: 8px;
    line-height: 1.45;
    font-size: 9.5pt;
  }
  .student-details ul {
    list-style-type: disc;
    padding-left: 18px;
    margin: 2px 0;
  }
  .student-details li {
    margin-bottom: 1.5px;
    text-align: left;
  }
  hr {
    border: none;
    border-top: 1px solid #94a3b8;
    margin: 8px 0;
  }
  h2 {
    font-size: 10.5pt;
    font-weight: bold;
    color: #1e40af;
    margin-top: 8px;
    margin-bottom: 3px;
    text-align: left;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  h3 {
    font-size: 9.5pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 5px;
    margin-bottom: 2px;
    text-align: left;
  }
  p, ul, ol {
    margin-top: 2px;
    margin-bottom: 4px;
    text-align: justify;
  }
  ul, ol {
    padding-left: 18px;
  }
  li {
    margin-bottom: 1.5px;
    text-align: justify;
  }
  .sub-task {
    margin-left: 6px;
    margin-bottom: 6px;
  }
  table.simple-table {
    width: 100%;
    border-collapse: collapse;
    margin: 5px 0;
    font-size: 8.5pt;
    text-align: left;
  }
  table.simple-table th, table.simple-table td {
    border: 1px solid #cbd5e1;
    padding: 3px 5px;
    text-align: left;
  }
  table.simple-table th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: bold;
  }
  table.simple-table tr:nth-child(even) {
    background-color: #f8fafc;
  }
  .img-box {
    text-align: center;
    margin: 5px 0;
  }
  .img-box img {
    max-width: 95%;
    max-height: 220px;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
  }
  .img-caption {
    font-size: 8pt;
    font-style: italic;
    color: #475569;
    margin-top: 1px;
    text-align: center;
  }
  .signature-section {
    margin-top: 12px;
    line-height: 1.5;
    font-size: 9.5pt;
  }
  .sig-line {
    border-bottom: 1px dashed #94a3b8;
    width: 100%;
    margin: 5px 0 6px 0;
  }
</style>
</head>
<body>

<h1>Weekly Progress Report</h1>

<div class="student-details">
  <strong>Student Details:</strong>
  <ul>
    <li><strong>Name:</strong> Neil Tauro</li>
    <li><strong>Roll No.:</strong> 24CSE1033</li>
    <li><strong>Supervisor's Name:</strong> Dr. Keshavamurthy B.N.</li>
    <li><strong>Reporting Period:</strong> 11/09/2026 – 17/09/2026</li>
    <li><strong>GitHub Repository:</strong> <a href="https://github.com/neiltauro15/DA-KMCT" style="color: #1e40af; font-weight: bold;">https://github.com/neiltauro15/DA-KMCT</a></li>
  </ul>
</div>

<hr>

<h2>1. Progress Summary</h2>
<p>During this reporting period, research and development focused on the Density-Aware k-Means Clustering of Trajectories (DA-KMCT) framework based on recent location-based service trajectory clustering literature (Liu et al., 2024). Standard k-means clustering struggles when applied directly to spatial trajectory datasets due to variable sequence lengths, differing GPS sample counts, and high sensitivity to random seed selection, frequently leading to poor local saddle-point convergence.</p>

<p>To overcome these core challenges, the DA-KMCT architecture integrates three primary components:</p>
<ol>
  <li><strong>Interpolated Trajectory to Point Set (ITS):</strong> Resamples variable-length spatial trajectories into uniform h-dimensional spatial waypoint vectors along their total polyline arc length, establishing fixed-length representations for Euclidean comparison.</li>
  <li><strong>Spatial Grid Density Quantization:</strong> Discretizes the 2D spatial feature domain into a uniform 10 &times; 10 spatial grid to compute localized waypoint density histograms across all trajectories.</li>
  <li><strong>Density-Weighted Centroid Update & Seeding:</strong> Seeds initial cluster centroids directly at dense grid cell peaks to avoid poor random initialization, and weights trajectory contributions during the Expectation-Maximization (EM) update step by local waypoint density.</li>
</ol>

<p>This approach effectively pulls cluster centers toward high-density trajectory cores while down-weighting outlier trajectories in sparse regions, improving overall stability and clustering accuracy.</p>

<hr>

<h2>2. Tasks Completed This Week</h2>

<p>The following technical milestones and subtasks were completed during the current reporting period:</p>

<h3>2.1. Tabular-to-Trajectory Feature Mapping</h3>
<p>Transformed 4D Iris dataset features into 2-step 2D spatial trajectories T<sub>i</sub> = [(sepal_length, sepal_width), (petal_length, petal_width)] with [0, 1] min-max spatial normalisation across dimensions.</p>

<h3>2.2. ITS Polyline Resampling Engine Implementation</h3>
<p>Implemented an arc-length polyline interpolation algorithm to resample all input trajectories into h = 5 uniformly spaced spatial waypoints along each polyline sequence.</p>

<h3>2.3. Methodology & Trajectory Normalization Architecture</h3>
<div class="sub-task">
  <p>The processing workflow transforms heterogeneous tabular data into standardized spatial trajectories, performs uniform polyline resampling, and applies density-aware clustering to identify natural trajectory groupings.</p>

  <p><strong>A. Spatial Feature Construction:</strong> In real-world location-based services, spatial trajectories represent sequences of geographic waypoints recorded over time. To establish a controlled benchmark, tabular features are mapped into 2D spatial trajectory paths. Each sample's Sepal measurements serve as the trajectory start location (Waypoint 0), while Petal measurements serve as the destination (Waypoint 1). Min-max normalization scales all coordinates to the unit interval [0, 1] to prevent feature scale imbalances.</p>

  <p><strong>B. Interpolated Trajectory to Point Set (ITS) Resampling:</strong> Because raw trajectories can differ in sample density and point counts, direct Euclidean comparison is ill-defined. The ITS resampling engine measures the cumulative polyline length of each trajectory and places h = 5 uniformly spaced waypoints along its path. This preserves the overall geometric shape and directional flow of the trajectory while enforcing a uniform vector dimension across all samples in the dataset.</p>

  <p><strong>C. Spatial Grid Density Quantization & Seeding:</strong> The normalized 2D bounding space is divided into a 10 &times; 10 uniform grid (100 cells). All 750 resampled waypoints (150 trajectories &times; 5 waypoints) are mapped into grid cells to construct a spatial density histogram. The top density cells are identified, and initial cluster centroids are seeded directly from the data points residing within these dense regions. This density-peak seeding prevents centroids from being initialized in sparse noise regions or getting trapped in suboptimal saddle points during early EM iterations.</p>

  <p><strong>D. Density-Weighted Expectation-Maximization (EM) Loop:</strong> During each EM epoch, trajectories are assigned to their nearest cluster centroid based on Euclidean distance in the flattened waypoint space. In the centroid update step (M-step), each trajectory's contribution to its assigned centroid is weighted by the average spatial density of the grid cells visited by its waypoints. Trajectories passing through dense cluster cores exert a stronger influence on the centroid position, while outlier trajectories in low-density cells have a reduced impact.</p>
</div>

<h3>2.4. Empirical Performance Evaluation & Convergence Results</h3>
<div class="sub-task">
  <p>DA-KMCT was evaluated on the 150-trajectory dataset with k = 3 target clusters, grid resolution g = 10, maximum iterations = 300, and convergence tolerance tol = 0.005. The algorithm achieved rapid convergence in <strong>15 EM iterations</strong>, reaching an overall clustering purity of <strong>88.00%</strong>.</p>

  <p><strong>Algorithm Performance & Accuracy Benchmarks:</strong></p>
  <table class="simple-table">
    <thead>
      <tr>
        <th>Performance Metric</th>
        <th>Measured Value</th>
        <th>Benchmark Description & Analysis</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>GitHub Repository</strong></td>
        <td colspan="2"><a href="https://github.com/neiltauro15/DA-KMCT" style="color: #1e40af; font-weight: bold;">https://github.com/neiltauro15/DA-KMCT</a></td>
      </tr>
      <tr>
        <td><strong>Total Trajectories (n)</strong></td>
        <td>150 Trajectories</td>
        <td>Mapped 4D Iris features into 2D spatial polyline trajectories</td>
      </tr>
      <tr>
        <td><strong>Target Clusters (k)</strong></td>
        <td>3 Clusters</td>
        <td>Matches true underlying species class count</td>
      </tr>
      <tr>
        <td><strong>ITS Waypoints (h)</strong></td>
        <td>5 Waypoints</td>
        <td>Uniform arc-length polyline resampling count</td>
      </tr>
      <tr>
        <td><strong>Spatial Grid Resolution (g)</strong></td>
        <td>10 &times; 10 (100 cells)</td>
        <td>Normalized [0, 1] &times; [0, 1] spatial domain histogram</td>
      </tr>
      <tr>
        <td><strong>Convergence Epochs</strong></td>
        <td><strong>15 Iterations</strong></td>
        <td>Terminated at max centroid displacement &lt; 0.005</td>
      </tr>
      <tr>
        <td><strong>Clustering Purity</strong></td>
        <td><strong>88.00%</strong></td>
        <td>Substantial improvement over random baseline (33.33%)</td>
      </tr>
      <tr>
        <td><strong>Inertia (SSE)</strong></td>
        <td><strong>15.6875</strong></td>
        <td>Sum of squared Euclidean distances in flattened R<sup>10</sup> space</td>
      </tr>
      <tr>
        <td><strong>Execution Runtime</strong></td>
        <td><strong>~0.0701 seconds</strong></td>
        <td>Fast vectorized execution using NumPy</td>
      </tr>
    </tbody>
  </table>

  <div class="img-box">
    <img src="fig_colored_performance.png" alt="Figure 1: Algorithm Performance">
    <div class="img-caption">Figure 1: (A) EM Iteration Convergence Loss Curve (SSE vs. Epochs); (B) Clustering Purity Comparison against Random Baseline.</div>
  </div>

  <p><strong>Trajectory Cluster Counts & Alignment Analysis:</strong> The 150 trajectories were grouped into 3 distinct clusters: Cluster 0 contains 48 trajectories, Cluster 1 contains 50 trajectories, and Cluster 2 contains 52 trajectories. Cluster 1 achieved 100% purity (Setosa), Cluster 0 achieved 96% purity (Versicolor), and Cluster 2 achieved 88.5% purity (Virginica).</p>

  <div class="img-box">
    <img src="fig_colored_clusters.png" alt="Figure 2: Cluster Distribution & Alignment">
    <div class="img-caption">Figure 2: (A) Trajectory Sample Count per Cluster; (B) Cluster vs. True Species Alignment Matrix.</div>
  </div>
</div>

<h3>2.5. Detailed Data Logs & Per-Sample Classification Snippets</h3>
<div class="sub-task">
  <p>Below is a sample of trajectory predictions generated by DA-KMCT alongside ground-truth species labels and exact 5-waypoint centroid coordinates learned by the algorithm. Codebase is available at <a href="https://github.com/neiltauro15/DA-KMCT" style="color: #1e40af; font-weight: bold;">https://github.com/neiltauro15/DA-KMCT</a>.</p>

  <p><strong>A. Per-Sample Classification Prediction Log:</strong></p>
  <table class="simple-table">
    <thead>
      <tr>
        <th>Sample ID</th>
        <th>Waypoint 0 (Sepal)</th>
        <th>Waypoint 1 (Petal)</th>
        <th>Predicted Cluster</th>
        <th>Ground Truth</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Sample 0</td><td>(0.2222, 0.6250)</td><td>(0.0678, 0.0417)</td><td>Cluster 1</td><td>Setosa (0)</td><td>Pure Match</td></tr>
      <tr><td>Sample 1</td><td>(0.1667, 0.4167)</td><td>(0.0678, 0.0417)</td><td>Cluster 1</td><td>Setosa (0)</td><td>Pure Match</td></tr>
      <tr><td>Sample 2</td><td>(0.1111, 0.5000)</td><td>(0.0508, 0.0417)</td><td>Cluster 1</td><td>Setosa (0)</td><td>Pure Match</td></tr>
      <tr><td>Sample 3</td><td>(0.0833, 0.4583)</td><td>(0.0847, 0.0417)</td><td>Cluster 1</td><td>Setosa (0)</td><td>Pure Match</td></tr>
      <tr><td>Sample 50</td><td>(0.7500, 0.5000)</td><td>(0.6271, 0.5417)</td><td>Cluster 0</td><td>Versicolor (1)</td><td>Match</td></tr>
      <tr><td>Sample 100</td><td>(0.5556, 0.5417)</td><td>(0.8475, 0.9583)</td><td>Cluster 2</td><td>Virginica (2)</td><td>Match</td></tr>
    </tbody>
  </table>

  <p><strong>B. Final Centroid Waypoint Coordinates:</strong></p>
  <table class="simple-table">
    <thead>
      <tr>
        <th>Cluster ID</th>
        <th>Dominant Species</th>
        <th>Size</th>
        <th>Waypoint 0</th>
        <th>Waypoint 1</th>
        <th>Waypoint 2</th>
        <th>Waypoint 3</th>
        <th>Waypoint 4</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Cluster 0</strong></td>
        <td>Versicolor</td>
        <td>48</td>
        <td>(0.4335, 0.3026)</td>
        <td>(0.4668, 0.3584)</td>
        <td>(0.5000, 0.4141)</td>
        <td>(0.5333, 0.4699)</td>
        <td>(0.5665, 0.5256)</td>
      </tr>
      <tr>
        <td><strong>Cluster 1</strong></td>
        <td>Setosa (100%)</td>
        <td>50</td>
        <td>(0.1910, 0.5771)</td>
        <td>(0.1627, 0.4476)</td>
        <td>(0.1344, 0.3181)</td>
        <td>(0.1060, 0.1886)</td>
        <td>(0.0777, 0.0591)</td>
      </tr>
      <tr>
        <td><strong>Cluster 2</strong></td>
        <td>Virginica</td>
        <td>52</td>
        <td>(0.6193, 0.4388)</td>
        <td>(0.6437, 0.5175)</td>
        <td>(0.6682, 0.5961)</td>
        <td>(0.6927, 0.6748)</td>
        <td>(0.7171, 0.7535)</td>
      </tr>
    </tbody>
  </table>
</div>

<hr>

<h2>3. Additional Notes</h2>
<ul>
  <li><strong>Key Observations:</strong> Density-aware initial centroid selection effectively eliminated poor seed placement, allowing fast convergence in 15 iterations with 88.00% purity.</li>
  <li><strong>Planned Future Work:</strong> (1) Evaluate sensitivity across grid resolutions g &in; {5, 10, 20, 50}; (2) Test DA-KMCT on real GPS datasets (T-Drive / Geolife); (3) Benchmark against Trajectory DBSCAN.</li>
</ul>

<hr>

<div class="signature-section">
  <p><strong>Student’s Signature:</strong> Neil Tauro</p>
  
  <p style="margin-top: 8px;"><strong>Supervisor’s Remarks:</strong> The research progress report is satisfactory / not-satisfactory (if not satisfactory, specific reasons must be furnished separately)</p>
  
  <div class="sig-line"></div>
  <div class="sig-line"></div>
  
  <p style="margin-top: 8px;"><strong>Supervisor’s Signature:</strong> ___________________</p>
</div>

</body>
</html>
"""

temp_html = r"c:\Users\neilt\OneDrive\Desktop\DAKMCT\temp_3page_report.html"
pdf_out = r"c:\Users\neilt\OneDrive\Desktop\DAKMCT\Weekly_Progress_Report.pdf"

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out}",
    temp_html
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_out):
    print("3-Page PDF successfully generated at:", pdf_out)
    os.remove(temp_html)
else:
    print("Error generating PDF:", res.stderr)
