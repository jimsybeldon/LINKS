import sys, os
import pickle
import numpy as np

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
# Show first few trajectory points for joint 0
# ------------------------------------------------------------
print("\nTrajectory for joint 0 (first 5 time steps):")
print(x[0][:5])

# ------------------------------------------------------------
# Normalize a coupler curve
# ------------------------------------------------------------
moving_nodes = np.where(node_types == 0)[0]
curve = x[moving_nodes[0]]   # pick first moving joint

norm = curve_normalizer()
curve_norm = norm(curve)

print("\n=== NORMALIZED CURVE ===")
print("Normalized curve shape:", curve_norm.shape)
print("First 10 normalized points:")
print(curve_norm[:10])
