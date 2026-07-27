# LINKS: A dataset of a hundred million planar linkage mechanisms for data-driven kinematic design

<img width="100%" src="https://i.ibb.co/BCPTFt0/overview-1.jpg" alt="overview">

Here you will find the code used to generate the dataset and simulate it.

## Required packages

- tensorflow > 2.4.0
- sklearn
- numpy
- matplotlib
- tqdm
- svgpath2mpl

## Dataset

The dataset is publicly available on Hugging Face: [ahn1376/LINKS-10M](https://huggingface.co/datasets/ahn1376/LINKS-10M)

### Dataset Description
The dataset is provided in 4 files. The mechanisms in the "dataset" file, the numerical simulation data for each mechanism in the "simulation_dataset" file and the dataset of the normalized curves in the "normalized_dataset" file, and the curated normalized curves in the "curated_dataset" file.

For more details on the structure of the data and use of our utility functions see the jupyter notebook in the Dataset folder.

### Code Details
The code provided here includes all the parts needed to open and simulate the mechanisms in the dataset. See Dataset.ipynb in the dataset folder for examples.

Note that the GPU solvers are also included in the sim.py but not used directly in the code.

### Project Page
<a href="https://decode.mit.edu/projects/LINKS">Project Page</a>

## Citation

If you use this dataset, please cite:

```bibtex
@proceedings{10.1115/DETC2022-89798,
    author = {Heyrani Nobari, Amin and Srivastava, Akash and Gutfreund, Dan and Ahmed, Faez},
    title = {LINKS: A Dataset of a Hundred Million Planar Linkage Mechanisms for Data-Driven Kinematic Design},
    volume = {Volume 3A: 48th Design Automation Conference (DAC)},
    series = {International Design Engineering Technical Conferences and Computers and Information in Engineering Conference},
    pages = {V03AT03A013},
    year = {2022},
    month = {08},
    doi = {10.1115/DETC2022-89798},
    url = {https://doi.org/10.1115/DETC2022-89798},
    eprint = {https://asmedigitalcollection.asme.org/IDETC-CIE/proceedings-pdf/IDETC-CIE2022/86229/V03AT03A013/6943011/v03at03a013-detc2022-89798.pdf},
}
```
