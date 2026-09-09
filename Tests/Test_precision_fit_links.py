import sys, os
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Ensure project root is on sys.path so "from LINKS import *" works
# ------------------------------------------------------------
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

from LINKS import *
from utils import curve_normalizer

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
dataset_path = os.path.join(project_root, "Dataset", "dataset")
precision_json_path = os.path.join(project_root, "Data", "precision_task_no_theta.json")

print("Loading dataset from:", dataset_path)
with open(dataset_path, "rb") as f:
    mechs = pickle.load(f)
print("Number of mechanisms in dataset:", len(mechs))

print("Loading precision task from:", precision_json_path)
with open(precision_json_path, "r") as f:
    pdata = json.load(f)

precision_points_all = np.array(pdata["precision_points"])  # shape (N, 2)
print("\n=== RAW PRECISION DATA ===")
print(precision_points_all)

# ------------------------------------------------------------
# User selects number of precision points: 2 or 3
# 2 -> first and last
# 3 -> all three in order
# ------------------------------------------------------------
num_pts = int(input("\nEnter 2 or 3 for number of precision points: ").strip())
if num_pts not in (2, 3):
    raise ValueError("Must enter 2 or 3.")

if num_pts == 2:
    P = np.vstack([precision_points_all[0], precision_points_all[-1]])
else:
    if precision_points_all.shape[0] < 3:
        raise ValueError("JSON does not contain 3 precision points.")
    P = precision_points_all[:3]

print("\nUsing precision points:")
print(P)

# ------------------------------------------------------------
# User selects bar count: 4 or 6 (filter by number of links)
# Option B: number of links = number of nonzero entries in A / 2
# ------------------------------------------------------------
bar_choice = int(input("\nEnter 4 or 6 for bar count (filter by number of links): ").strip())
## if bar_choice not in (4, 6):
##     raise ValueError("Must enter 4 or 6.")

print(f"\nMechanism type selected: {bar_choice}-bar (by link count)")

# ------------------------------------------------------------
# Helper: count links from adjacency matrix
# ------------------------------------------------------------
def count_links(A):
    # Undirected graph: each link appears twice in A (i,j) and (j,i)
    return int(np.count_nonzero(A) // 2)

# ------------------------------------------------------------
# Helper: compute error between precision points and normalized coupler curve
# Strategy: for each precision point, find nearest point on curve_norm
# error = sum of squared distances
# ------------------------------------------------------------
def curve_fit_error(curve_norm, P):
    # curve_norm: (T, 2)
    # P: (M, 2)
    err = 0.0
    for p in P:
        # distances to all points on curve
        d2 = np.sum((curve_norm - p) ** 2, axis=1)
        err += np.min(d2)
    return err

# ------------------------------------------------------------
# Helper: extract link lengths from A and x0
# ------------------------------------------------------------
def extract_links(A, x0):
    N = A.shape[0]
    links = []
    for i in range(N):
        for j in range(i + 1, N):
            if A[i, j] != 0:
                length = np.linalg.norm(x0[i] - x0[j])
                links.append((i, j, length))
    return links

# ------------------------------------------------------------
# Search over dataset for best-fit mechanism
# ------------------------------------------------------------
norm = curve_normalizer()

best_err = np.inf
best_idx = None
best_data = None  # (A, x0, node_types, curve, curve_norm, fixed_nodes, coupler_idx)

thetas = np.linspace(0, 2 * np.pi, 200)
motor = [0, 1]

print("\n=== SEARCHING DATASET FOR BEST FIT ===")

for i, mech in enumerate(mechs):
    A, x0, node_types = mech

    # Filter by number of links (Option B)
    n_links = count_links(A)
    if n_links > bar_choice:
        continue

    fixed_nodes = np.where(node_types)[0]

    # Dyadic path
    path, ok = find_path(A, motor=motor, fixed_nodes=fixed_nodes)
    if not ok:
        continue

    # Solve full revolution
    G = get_G(x0)
    try:
        x, valid, locking_joint = solve_rev_vectorized(path, x0, G, motor, fixed_nodes, thetas)
    except Exception:
        continue

    if not valid.all():
        continue

    # Pick coupler point: first moving joint
    moving_nodes = np.where(node_types == 0)[0]
    if len(moving_nodes) == 0:
        continue
    coupler_idx = moving_nodes[0]

    curve = x[coupler_idx]  # (T, 2)
    curve_norm = norm(curve)

    # Compute error to precision points
    err = curve_fit_error(curve_norm, P)

    if err < best_err:
        best_err = err
        best_idx = i
        best_data = (A, x0, node_types, curve, curve_norm, fixed_nodes, coupler_idx)

        print(f"New best: mech {i}, links={n_links}, error={err:.6f}")

# ------------------------------------------------------------
# Report best mechanism
# ------------------------------------------------------------
if best_idx is None:
    print("\nNo valid mechanism found matching bar_choice and precision points.")
    sys.exit(0)

A_best, x0_best, node_types_best, curve_best, curve_norm_best, fixed_nodes_best, coupler_idx_best = best_data

print("\n=== BEST-FIT MECHANISM ===")
print(f"Mechanism index: {best_idx}")
print(f"Bar count (links): {count_links(A_best)}")
print(f"Fit error: {best_err:.6f}")

print("\nAdjacency matrix A:")
print(A_best)

print("\nInitial joint positions x0:")
print(x0_best)

print("\nNode types (True=fixed, False=moving):")
print(node_types_best)

# ------------------------------------------------------------
# Extract and print link lengths
# ------------------------------------------------------------
links = extract_links(A_best, x0_best)
print("\n=== LINK LENGTHS ===")
for k, (i, j, L) in enumerate(links, start=1):
    print(f"Link{k}: joints {i}–{j}, length = {L:.6f}")

# ------------------------------------------------------------
# Plot best mechanism with coupler curve and precision points
# ------------------------------------------------------------
def plot_mech(A, x_t, fixed_nodes=None, coupler_idx=None, title=None):
    N = A.shape[0]
    for i in range(N):
        for j in range(i + 1, N):
            if A[i, j] != 0:
                xi, yi = x_t[i]
                xj, yj = x_t[j]
                plt.plot([xi, xj], [yi, yj], 'k-', linewidth=1)

    xs = x_t[:, 0]
    ys = x_t[:, 1]

    if fixed_nodes is not None and len(fixed_nodes) > 0:
        moving_mask = np.ones(N, dtype=bool)
        moving_mask[fixed_nodes] = False
        plt.scatter(xs[fixed_nodes], ys[fixed_nodes], c='r', s=40, label='fixed')
        plt.scatter(xs[moving_mask], ys[moving_mask], c='b', s=30, label='moving')
    else:
        plt.scatter(xs, ys, c='b', s=30)

    if coupler_idx is not None:
        plt.scatter(x_t[coupler_idx, 0], x_t[coupler_idx, 1],
                    c='g', s=60, marker='o', label='coupler point')

    if title is not None:
        plt.title(title)
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best', fontsize=8)

# initial configuration
plt.figure(figsize=(6, 6))
plot_mech(A_best, x0_best, fixed_nodes=fixed_nodes_best,
          coupler_idx=coupler_idx_best,
          title=f"Best Mechanism #{best_idx} - Initial Configuration")
plt.scatter(P[:, 0], P[:, 1], c='m', s=60, marker='x', label='precision points')
plt.legend(loc='best', fontsize=8)
plt.show()

# full coupler curve
plt.figure(figsize=(6, 6))
plot_mech(A_best, x0_best, fixed_nodes=fixed_nodes_best,
          coupler_idx=coupler_idx_best,
          title=f"Best Mechanism #{best_idx} with Coupler Curve")
plt.plot(curve_best[:, 0], curve_best[:, 1], 'r-', linewidth=2, label='coupler curve')
plt.scatter(P[:, 0], P[:, 1], c='m', s=60, marker='x', label='precision points')
plt.legend(loc='best', fontsize=8)
plt.show()

# normalized coupler curve vs precision points
plt.figure(figsize=(6, 6))
plt.plot(curve_norm_best[:, 0], curve_norm_best[:, 1], 'b-', linewidth=2, label='normalized coupler curve')
plt.scatter(P[:, 0], P[:, 1], c='m', s=60, marker='x', label='precision points')
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.title("Normalized Coupler Curve vs Precision Points")
plt.legend(loc='best', fontsize=8)
plt.show()
