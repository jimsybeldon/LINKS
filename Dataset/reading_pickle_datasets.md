An **HDF5 dataset file** is a *hierarchical, binary container format* for storing large numerical data.  
But **your LINKS files (`dataset`, `simulation_dataset`, etc.) are *not* HDF5 files** — they are **plain pickle files** even though the authors casually call them “HDF5 dataset files.”

Let me explain both clearly so you know exactly what you’re dealing with and how to inspect them.

---

# ✅ Part 1 — What an actual HDF5 file is  
HDF5 is a **hierarchical data format** used for scientific datasets.  
It behaves like a **filesystem inside a single file**:

- **Groups** (like folders)
- **Datasets** (like NumPy arrays)
- **Attributes** (metadata)
- **Compression**
- **Partial reads** (load slices without loading whole dataset)

You can inspect real HDF5 files using tools like:

- **h5py** (Python)
- **HDFView** (GUI)   [The HDF Group](https://www.hdfgroup.org/download-hdfview/)


- **h5web** (VSCode/Jupyter extension)

HDFView shows the file as a tree structure and lets you browse datasets and metadata.  
This is described in the HDFView documentation: it lets you *view a file hierarchy in a tree structure, create new files, add/delete groups and datasets, and view/modify dataset content*   [The HDF Group](https://www.hdfgroup.org/download-hdfview/).

---

# ❗ Part 2 — Your LINKS files are **not HDF5**  
Even though the README calls them “HDF5 dataset files,” the code proves they are **pickle streams**:

```python
mechanism_file = open(b"dataset","rb")
mechs = pickle.load(mechanism_file)
```

This is **not** how HDF5 files are opened.  
HDF5 requires `h5py.File(...)`.

So your files:

- `dataset`
- `simulation_dataset`
- `normalized_dataset`
- `curated_dataset`

are **just binary pickle files containing Python lists**.

You cannot open them with HDFView or h5py.

You *must* use Python’s `pickle.load`.

---

# ✅ Part 3 — How to inspect your LINKS dataset files

### ✔ Option A — Inspect with Python (correct for LINKS)

```python
import pickle

with open("dataset", "rb") as f:
    mechs = pickle.load(f)

print(type(mechs))
print(len(mechs))
print(type(mechs[0]))
```

You will see:

- `mechs` is a **list**
- length ≈ 100,000
- each entry is a **tuple**: `(A, x0, node_types)`

To inspect one mechanism:

```python
A, x0, node_types = mechs[0]

print(A.shape)        # adjacency matrix
print(x0.shape)       # joint positions
print(node_types)     # fixed/moving flags
```

To inspect normalized curves:

```python
with open("normalized_dataset", "rb") as f:
    nsols = pickle.load(f)

curve, mech_i, node_i = nsols[0]
print(curve.shape)
print(mech_i, node_i)
```

---

# ✔ Option B — If you *did* have a real HDF5 file  
You would inspect it using **h5py**:

```python
import h5py

with h5py.File("file.h5", "r") as f:
    print(list(f.keys()))
    data = f["dataset_name"][:]
```

Or visually using **HDFView**, which shows:

- tree hierarchy  
- groups  
- datasets  
- metadata  

As described in the HDFView guide: it displays the file structure in a tree panel and lets you view metadata and dataset contents   [portal.hdfgroup.org](https://portal.hdfgroup.org/documentation/hdfview/latest/ug02start.html).

But again — **your LINKS files are not HDF5**, so this does not apply.

---

# 🎯 Summary

### ✔ HDF5 is a hierarchical scientific data format  
### ✔ HDFView and h5py can inspect real HDF5 files  
### ❗ LINKS dataset files are *not* HDF5 — they are pickle lists  
### ✔ You must inspect them using `pickle.load`  
### ✔ Each file contains 100,000 Python objects (mechanisms, simulations, curves)

---

If you want, I can also show you:

- how to convert the LINKS pickle files *into* real HDF5 files  
- how to browse mechanisms interactively in a Jupyter notebook  
- how to build a PyCharm tool window to inspect mechanisms visually  

Just tell me what direction you want next.