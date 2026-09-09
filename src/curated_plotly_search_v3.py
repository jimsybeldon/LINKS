from pathlib import Path
import pickle
import numpy as np
import matplotlib.pyplot as plt

script_location = Path(__file__).resolve()
data_path = script_location.parent.parent / "Dataset" / "curated_dataset"

print(f"Loading dataset from: {data_path}")
with open(data_path, "rb") as f:
    raw_data = pickle.load(f)

total_curves = len(raw_data)
grid_size = 10  # 10x10 = 100 curves per page
batch_size = grid_size * grid_size
current_start = 0


def extract_pts(entry):
    for sub_item in entry:
        try:
            arr = np.asarray(sub_item, dtype=float)
            if arr.ndim == 2 and arr.shape[1] == 2:
                return arr
            elif arr.ndim == 1 and len(arr) % 2 == 0 and len(arr) > 4:
                return arr.reshape(-1, 2)
        except Exception:
            continue
    return None


while True:
    fig, axes = plt.subplots(grid_size, grid_size, figsize=(14, 14))
    end_idx = min(current_start + batch_size, total_curves)

    for i, ax in enumerate(axes.flat):
        idx = current_start + i
        if idx >= total_curves:
            ax.axis("off")
            continue

        pts = extract_pts(raw_data[idx])
        if pts is not None:
            ax.plot(pts[:, 0], pts[:, 1], color="#1f77b4", linewidth=0.8)
            ax.set_title(f"#{idx}", fontsize=7, pad=1)

        ax.set_aspect("equal", adjustable="datalim")
        ax.axis("off")

    plt.tight_layout()
    plt.suptitle(f"Curves {current_start} to {end_idx - 1} of {total_curves}", y=1.01, fontsize=12)
    plt.show(block=False)
    plt.pause(0.1)

    # Command loop in console
    user_input = input("\n[n]ext page | [p]revious page | enter index number | [q]uit: ").strip().lower()
    plt.close(fig)

    if user_input == "n":
        if current_start + batch_size < total_curves:
            current_start += batch_size
        else:
            print("Reached the end of the dataset.")
    elif user_input == "p":
        current_start = max(0, current_start - batch_size)
    elif user_input.isdigit():
        target = int(user_input)
        if 0 <= target < total_curves:
            current_start = (target // batch_size) * batch_size
        else:
            print(f"Index out of bounds (0 to {total_curves - 1}).")
    elif user_input == "q":
        break