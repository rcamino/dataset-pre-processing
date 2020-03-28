# dataset-pre-processing

Pre-processing of popular datasets (from UCI repositories for now). The methods include:

- One-hot-encoding of categorical variables
- Min-max-scaling of numerical variables into the range [0, 1]
- Generating metadata information:
  - Number of samples
  - Number of features
  - Variable types
  - One-hot-encoding dictionaries
  - Class names
  
 Scripts for downloading datasets and pre-processing them with default parameters are also included.

## Pre-requisites

The project was developed using python 2.7.12 with the following packages:

- numpy==1.15.1
- scikit-learn==0.19.2
- scipy==1.1.0

This is needed only for downloading and extracting compressed file contents:
- wget==3.2
- xlrd==1.1.0

Installation with pip:

```bash
pip install -r requirements.txt
```
