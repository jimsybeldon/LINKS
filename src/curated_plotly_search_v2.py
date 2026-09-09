from pathlib import Path
import pickle
import numpy as np
import matplotlib.pyplot as plt

script_location = Path(__file__).resolve()
data_path = script_location.parent.parent / "Dataset" / "curated_dataset"

with open(data_path, "rb") as f:
    raw_data = pickle.load(f)

# Configure grid: e.g., 10x10 = 100 curves per view
grid_size = 10
start_idx = 0  # Change this offset to view subsequent batches (e.g., 100, 200, 300)
num_display = grid_size * grid_size

fig, axes = plt.subplots(grid_size, grid_size, figsize=(15, 15))

for i, ax in enumerate(axes.flat):
    idx = start_idx + i
    if idx >= len(raw_data):
        break

    entry = raw_data[idx]
    pts = None
    for sub_item in entry:
        try:
            arr = np.asarray(sub_item, dtype=float)
            if arr.ndim == 2 and arr.shape[1] == 2:
                pts = arr
                break
            elif arr.ndim == 1 and len(arr) % 2 == 0 and len(arr) > 4:
                pts = arr.reshape(-1, 2)
                break
        except Exception:
            continue

    if pts is not None:
        ax.plot(pts[:, 0], pts[:, 1], color="#1f77b4", linewidth=1.0)
        ax.set_title(f"#{idx}", fontsize=7, pad=2)

    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")

plt.tight_layout()
plt.suptitle(f"Curated Dataset Overview (Indices {start_idx} to {start_idx + num_display - 1})", y=1.01)
plt.show()