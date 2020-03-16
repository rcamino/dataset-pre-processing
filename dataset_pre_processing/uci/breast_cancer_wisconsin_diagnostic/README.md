# Breast Cancer Wisconsin (Diagnostic)

Source: https://archive.ics.uci.edu/ml/datasets/Breast%2BCancer%2BWisconsin%2B%28Diagnostic%29

Diagnostic Wisconsin Breast Cancer Database.

**WARNING**: can be confused with

* [Breast Cancer](https://archive.ics.uci.edu/ml/datasets/Breast%2BCancer)
* [Breast Cancer Wisconsin (Original)](https://archive.ics.uci.edu/ml/datasets/breast%2Bcancer%2Bwisconsin%2B%28original%29)
* [Breast Cancer Wisconsin (Prognostic)](https://archive.ics.uci.edu/ml/datasets/Breast%2BCancer%2BWisconsin%2B%28Prognostic%29)

## Samples

Number of samples: 569.

## Variables

| Numerical | Categorical | Binary | Total |
| :--- | :--- | :--- | :--- |
| 31 | 1 | 0 | 32 |

| Predictive | Non-Predictive | Target | Total |
| :--- | :--- | :--- | :--- |
| 30 | 1 | 1 | 32 |

The variable index corresponds to the order in the original data.

The corresponding feature index after the transformation may differ (check the metadata).

The target variable is "Diagnosis".

| Index | Name | Type | Description |
| :--- | :--- | :--- | :--- |
| 1 | ID number | numerical | |
| 2 | Diagnosis | categorical | |
| 3 | n1_radius | numerical | nucleus 1: mean of distances from center to points on the perimeter |
| 4 | n1_texture | numerical | nucleus 1: standard deviation of gray-scale values |
| 5 | n1_perimeter | numerical | nucleus 1: perimeter |
| 6 | n1_area | numerical | nucleus 1: area |
| 7 | n1_smoothness | numerical | nucleus 1: local variation in radius lengths |
| 8 | n1_compactness | numerical | nucleus 1: perimeter^2 / area - 1.0 |
| 9 | n1_concavity | numerical | nucleus 1: severity of concave portions of the contour |
| 10 | n1_concave_points | numerical | nucleus 1: number of concave portions of the contour |
| 11 | n1_symmetry | numerical | nucleus 1: symmetry |
| 12 | n1_fractal_dimension | numerical | nucleus 1: coastline approximation - 1 |
| 13 | n2_radius | numerical | nucleus 2: mean of distances from center to points on the perimeter |
| 14 | n2_texture | numerical | nucleus 2: standard deviation of gray-scale values |
| 15 | n2_perimeter | numerical | nucleus 2: perimeter |
| 16 | n2_area | numerical | nucleus 2: area |
| 17 | n2_smoothness | numerical | nucleus 2: local variation in radius lengths |
| 18 | n2_compactness | numerical | nucleus 2: perimeter^2 / area - 1.0 |
| 19 | n2_concavity | numerical | nucleus 2: severity of concave portions of the contour |
| 20 | n2_concave_points | numerical | nucleus 2: number of concave portions of the contour |
| 21 | n2_symmetry | numerical | nucleus 2: symmetry |
| 22 | n2_fractal_dimension | numerical | nucleus 2: coastline approximation - 1 |
| 23 | n3_radius | numerical | nucleus 3: mean of distances from center to points on the perimeter |
| 24 | n3_texture | numerical | nucleus 3: standard deviation of gray-scale values |
| 25 | n3_perimeter | numerical | nucleus 3: perimeter |
| 26 | n3_area | numerical | nucleus 3: area |
| 27 | n3_smoothness | numerical | nucleus 3: local variation in radius lengths |
| 28 | n3_compactness | numerical | nucleus 3: perimeter^2 / area - 1.0 |
| 29 | n3_concavity | numerical | nucleus 3: severity of concave portions of the contour |
| 30 | n3_concave_points | numerical | nucleus 3: number of concave portions of the contour |
| 31 | n3_symmetry | numerical | nucleus 3: symmetry |
| 32 | n3_fractal_dimension | numerical | nucleus 3: coastline approximation - 1 |


## Class distribution

| Value | Description | Samples |
| :--- | :--- | :--- |
| B | benign | 357 |
| M | malignant | 212 |