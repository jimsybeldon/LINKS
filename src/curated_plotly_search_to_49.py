from pathlib import Path
import pickle
import numpy as np
import plotly.graph_objects as go

# Breakdown of the Path Traversal
# Path(__file__).resolve() gets the absolute path of your script (.../LINKS/src/curated_plotly_search.py).
# .parent refers to the src folder (.../LINKS/src).
# .parent.parent moves up to the project root (.../LINKS).
# / "Dataset" / "curated_dataset" targets the file in the Dataset directory (.../LINKS/Dataset/curated_dataset).

data_path = Path(__file__).resolve().parent.parent / "Dataset" / "curated_dataset"

with open(data_path, "rb") as f:
    raw_data = pickle.load(f)

fig = go.Figure()
max_display = min(50, len(raw_data))

for idx in range(max_display):
    entry = raw_data[idx]

    # Identify which sub-item contains the N x 2 coordinate array
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

    if pts is None:
        continue

    fig.add_trace(
        go.Scatter(
            x=pts[:, 0],
            y=pts[:, 1],
            mode="lines",
            name=f"Curve {idx}",
            visible=(idx == 0)
        )
    )

buttons = []
for idx in range(len(fig.data)):
    mask = [False] * len(fig.data)
    mask[idx] = True
    buttons.append(
        dict(
            label=f"Curve #{idx}",
            method="update",
            args=[{"visible": mask}, {"title": f"Curated Curve #{idx}"}]
        )
    )

fig.update_layout(
    updatemenus=[dict(active=0, buttons=buttons, x=0.1, y=1.15)],
    yaxis=dict(scaleanchor="x", scaleratio=1),
    width=700,
    height=700
)

fig.show()