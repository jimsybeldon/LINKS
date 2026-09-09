import sys, os
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
# Load dataset file
# ------------------------------------------------------------
dataset_path = os.path.join(project_root, "Dataset", "dataset")

print("Loading dataset from:", dataset_path)

with open(dataset_path, "rb") as f:
    mechs = pickle.load(f)

print("Number of mechanisms in dataset:", len(mechs))

# ------------------------------------------------------------
# Extract mechanism #0
# ------------------------------------------------------------
A, x0, node_types = mechs[0]

print("\n=== RAW MECHANISM DATA ===")
print("\nAdjacency matrix A:")
print(A)

print("\nInitial joint positions x0:")
print(x0)

print("\nNode types (True=fixed, False=moving):")
print(node_types)

# ------------------------------------------------------------
# Dyadic path
# ------------------------------------------------------------
fixed_nodes = np.where(node_types)[0]
motor = [0, 1]

path, ok = find_path(A, motor=motor, fixed_nodes=fixed_nodes)

print("\n=== DYADIC SOLVE PATH ===")
print(path)
print("Path valid:", ok)

# ------------------------------------------------------------
# Solve full revolution
# ------------------------------------------------------------
G = get_G(x0)
thetas = np.linspace(0, 2*np.pi, 200)

x, valid, locking_joint = solve_rev_vectorized(path, x0, G, motor, fixed_nodes, thetas)

print("\n=== TRAJECTORY RESULTS ===")
print("Trajectory array shape (N, T, 2):", x.shape)
print("Validity flags for each time step:")
print(valid)
print("All valid:", valid.all())
print("Locking joint index:", locking_joint)

# ------------------------------------------------------------
# Pick a coupler point (first moving joint)
# ------------------------------------------------------------
moving_nodes = np.where(node_types == 0)[0]
coupler_idx = moving_nodes[0]
curve = x[coupler_idx]   # shape (T, 2)

norm = curve_normalizer()
curve_norm = norm(curve)

print("\n=== NORMALIZED CURVE ===")
print("Normalized curve shape:", curve_norm.shape)
print("First 10 normalized points:")
print(curve_norm[:10])

# ------------------------------------------------------------
# Simple plotting helper for the linkage
# ------------------------------------------------------------
def plot_mech(A, x_t, fixed_nodes=None, title=None):
    """
    A: (N, N) adjacency matrix
    x_t: (N, 2) joint coordinates at one time step
    fixed_nodes: indices of fixed joints (optional)
    """
    N = A.shape[0]

    # Draw links
    for i in range(N):
        for j in range(i + 1, N):
            if A[i, j] != 0:
                xi, yi = x_t[i]
                xj, yj = x_t[j]
                plt.plot([xi, xj], [yi, yj], 'k-', linewidth=1)

    # Draw joints
    xs = x_t[:, 0]
    ys = x_t[:, 1]

    if fixed_nodes is not None and len(fixed_nodes) > 0:
        moving_mask = np.ones(N, dtype=bool)
        moving_mask[fixed_nodes] = False

        # fixed joints: red
        plt.scatter(xs[fixed_nodes], ys[fixed_nodes], c='r', s=40, label='fixed')
        # moving joints: blue
        plt.scatter(xs[moving_mask], ys[moving_mask], c='b', s=30, label='moving')
    else:
        plt.scatter(xs, ys, c='b', s=30)

    # highlight coupler point
    plt.scatter(x_t[coupler_idx, 0], x_t[coupler_idx, 1],
                c='g', s=60, marker='o', label='coupler point')

    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    if title is not None:
        plt.title(title)
    plt.legend(loc='best', fontsize=8)

# ------------------------------------------------------------
# 1) Show initial configuration
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))
plot_mech(A, x0, fixed_nodes=fixed_nodes, title="Mechanism #0 - Initial Configuration")
plt.show()

# ------------------------------------------------------------
# 2) Animate mechanism + growing coupler curve
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))

for t in range(len(thetas)):
    plt.clf()

    # current configuration
    x_t = x[:, t, :]  # shape (N, 2)
    plot_mech(A, x_t, fixed_nodes=fixed_nodes,
              title=f"Mechanism #0 - t = {t}, theta = {thetas[t]:.2f} rad")

    # coupler curve up to time t
    plt.plot(curve[:t+1, 0], curve[:t+1, 1], 'r-', linewidth=2, label='coupler curve')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)

    plt.pause(0.01)

plt.show()

# ------------------------------------------------------------
# 3) Plot full coupler curve (static)
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))
plot_mech(A, x0, fixed_nodes=fixed_nodes, title="Mechanism #0 with Full Coupler Curve")
plt.plot(curve[:, 0], curve[:, 1], 'r-', linewidth=2, label='coupler curve')
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.legend(loc='best', fontsize=8)
plt.show()

# ------------------------------------------------------------
# 4) Plot normalized coupler curve alone
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))
plt.plot(curve_norm[:, 0], curve_norm[:, 1], 'b-', linewidth=2)
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.title("Normalized Coupler Curve")
plt.show()
