import sys, os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import json


# ------------------------------------------------------------
# Ensure project root is on sys.path so "from LINKS import *" works
# ------------------------------------------------------------
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)




# ------------------------------------------------------------
# Load precision point JSON
# ------------------------------------------------------------
with open("precision_task.json", "r") as f:
    data = json.load(f)

precision_points = np.array(data["precision_points"])   # shape (3,2)
theta_deg = np.array(data["theta_deg"])                 # shape (3,)

print("Loaded precision points:")
print(precision_points)
print("Loaded theta angles (deg):")
print(theta_deg)

# ------------------------------------------------------------
# User chooses 2 or 3 precision points
# ------------------------------------------------------------
num_pts = int(input("Enter 2 or 3 for number of precision points: "))

if num_pts not in (2,3):
    raise ValueError("Must enter 2 or 3.")

P = precision_points[:num_pts]
theta = theta_deg[:num_pts]

print("\nUsing precision points:")
print(P)
print("Using theta angles:")
print(theta)

# ------------------------------------------------------------
# User chooses mechanism type: 4, 6, or 8 bars
# ------------------------------------------------------------
bar_choice = int(input("Enter 4, 6, or 8 for bar count: "))

if bar_choice not in (4,6,8):
    raise ValueError("Must enter 4, 6, or 8.")

print(f"\nMechanism type selected: {bar_choice}-bar (or fewer)")

# ------------------------------------------------------------
# Build synthesis basis
# ------------------------------------------------------------
basis = {
    "points": P,
    "theta_deg": theta,
    "num_points": num_pts,
    "bar_choice": bar_choice
}

print("\n=== SYNTHESIS BASIS ===")
for k,v in basis.items():
    print(k, ":", v)

# ------------------------------------------------------------
# Placeholder: generate candidate mechanisms
# Replace this with your actual synthesis engine
# ------------------------------------------------------------
candidate_mechanisms = []   # list of dicts: {"bars": n, "params": ..., "error": ...}

# Example placeholder candidate (REMOVE THIS IN REAL USE)
candidate_mechanisms.append({
    "bars": bar_choice,
    "params": np.array([1,2,3]),   # placeholder
    "error": 0.123                 # placeholder
})

# ------------------------------------------------------------
# Rank candidates by error
# ------------------------------------------------------------
ranked = sorted(candidate_mechanisms, key=lambda c: c["error"])

print("\n=== RANKED CANDIDATES ===")
for c in ranked:
    print(f"{c['bars']}-bar candidate, error={c['error']}, params={c['params']}")

# ------------------------------------------------------------
# Optional: normalized visualization of precision points
# ------------------------------------------------------------
plt.figure(figsize=(5,5))
plt.scatter(P[:,0], P[:,1], c='r', s=60)
plt.title("Precision Points Used")
plt.axis('equal')
plt.grid(True)
plt.show()
