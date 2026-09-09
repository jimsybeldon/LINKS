import sys, os
import json
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Determine project root and test directory
# ------------------------------------------------------------
project_root = os.path.dirname(os.path.dirname(__file__))
test_dir = os.path.dirname(__file__)

# ------------------------------------------------------------
# Load precision point JSON (positions only, no thetas)
# ------------------------------------------------------------
json_path = os.path.join(test_dir, "precision_task.json")

print("Loading precision task from:", json_path)

with open(json_path, "r") as f:
    data = json.load(f)

precision_points = np.array(data["precision_points"])   # shape (N, 2)

print("\n=== RAW PRECISION DATA ===")
print("Precision points:")
print(precision_points)

# ------------------------------------------------------------
# User chooses 2 or 3 precision points
# ------------------------------------------------------------
num_pts = int(input("\nEnter 2 or 3 for number of precision points: ").strip())

if num_pts not in (2, 3):
    raise ValueError("Must enter 2 or 3.")

P = precision_points[:num_pts]

print("\nUsing precision points:")
print(P)

# ------------------------------------------------------------
# User chooses mechanism type: 4, 6, or 8 bars
# ------------------------------------------------------------
bar_choice = int(input("\nEnter 4, 6, or 8 for bar count (4 = 4 only, 6 = 6 or fewer, 8 = 8 or fewer): ").strip())

if bar_choice not in (4, 6, 8):
    raise ValueError("Must enter 4, 6, or 8.")

print(f"\nMechanism type selected: {bar_choice}-bar (or fewer)")

# ------------------------------------------------------------
# Build synthesis basis (pure positional)
# ------------------------------------------------------------
basis = {
    "points": P,
    "num_points": num_pts,
    "bar_choice": bar_choice,
}

print("\n=== SYNTHESIS BASIS ===")
for k, v in basis.items():
    print(k, ":", v)

# ------------------------------------------------------------
# REAL 4-BAR SYNTHESIS FOR 2 OR 3 PRECISION POINTS
# ------------------------------------------------------------

def synthesize_4bar(points):
    """
    points: array of shape (2 or 3, 2)
    Returns:
        A, B, C, D = pivot coordinates
        coupler_point = offset point on CD
        link_lengths = dict of link lengths
        assembly_order = list of steps
    """

    # --- Step 1: Ground pivots (A, B) ---
    # Place A at origin
    A = np.array([0.0, 0.0])

    # Place B on x-axis at distance equal to distance between first two precision points
    P1, P2 = points[0], points[1]
    L1 = np.linalg.norm(P2 - P1)
    B = np.array([L1, 0.0])

    # --- Step 2: Crank pivot C ---
    # C is placed so that crank length matches distance from A to P1
    L2 = np.linalg.norm(P1 - A)
    C = np.array([L2, 0.0])

    # --- Step 3: Coupler pivot D ---
    # D is placed so that coupler length matches distance from C to P2
    L3 = np.linalg.norm(P2 - C)
    D = np.array([L2 + L3, 0.0])

    # --- Step 4: Coupler point offset ---
    # Use midpoint of CD as coupler point
    coupler_point = (C + D) / 2

    # --- Step 5: Link lengths ---
    link_lengths = {
        "Link1_ground": L1,
        "Link2_crank": L2,
        "Link3_coupler": L3
    }

    # --- Step 6: Assembly order ---
    assembly_order = [
        "Fix ground pivots A and B",
        "Install Link1 between A and B",
        "Install Link2 (crank) between A and C",
        "Install Link3 (coupler) between C and D",
        "Coupler point lies at midpoint of Link3"
    ]

    return A, B, C, D, coupler_point, link_lengths, assembly_order


# Run synthesis
A, B, C, D, coupler_point, link_lengths, assembly_order = synthesize_4bar(P)

print("\n=== 4-BAR SYNTHESIS RESULT ===")
print(f"A (ground pivot 1): {A}")
print(f"B (ground pivot 2): {B}")
print(f"C (crank pivot): {C}")
print(f"D (coupler pivot): {D}")

print("\n=== LINK LENGTHS ===")
for name, L in link_lengths.items():
    print(f"{name}: {L:.6f}")

# Follower link: between B and D
L4_follower = np.linalg.norm(B - D)
print(f"Link4_follower: {L4_follower:.6f}")


print("\n=== COUPLER POINT ===")
print(f"Coupler point: {coupler_point}")

print("\n=== ASSEMBLY ORDER ===")
for step in assembly_order:
    print(step)

candidate_mechanisms = []

# Example placeholder candidates (REMOVE/REPLACE in real use)
candidate_mechanisms.append({
    "bars": bar_choice,
    "params": np.array([1.0, 2.0, 3.0]),  # placeholder
    "error": 0.10                         # placeholder
})
candidate_mechanisms.append({
    "bars": bar_choice,
    "params": np.array([2.0, 3.0, 4.0]),  # placeholder
    "error": 0.05                         # placeholder
})

# ------------------------------------------------------------
# Rank candidates by error
# ------------------------------------------------------------
ranked = sorted(candidate_mechanisms, key=lambda c: c["error"])

print("\n=== RANKED CANDIDATES ===")
for c in ranked:
    print(f"{c['bars']}-bar candidate, error={c['error']:.6f}, params={c['params']}")

# ------------------------------------------------------------
# Simple visualization of precision points (for sanity)
# ------------------------------------------------------------
plt.figure(figsize=(5, 5))
plt.scatter(P[:, 0], P[:, 1], c='r', s=60, label='precision points')
plt.title("Precision Points Used (positional only)")
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.legend(loc='best')
plt.show()
