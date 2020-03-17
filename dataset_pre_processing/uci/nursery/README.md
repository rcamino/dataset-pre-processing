# Nursery

Nursery Database was derived from a hierarchical decision model originally developed to rank applications for nursery schools.
[[Source]](https://archive.ics.uci.edu/ml/datasets/Nursery)

## Samples

Number of samples: 12,960.

## Variables

| Numerical | Categorical | Binary | Total |
| :--- | :--- | :--- | :--- |
| 0 | 9 | 0 | 9 |

| Predictive | Non-Predictive | Target | Total |
| :--- | :--- | :--- | :--- |
| 8 | 0 | 1 | 9 |

The variable index corresponds to the order in the original data.

The corresponding feature index after the transformation may differ (check the metadata).

The target variable is "class".

| Index | Name | Type | Description |
| :--- | :--- | :--- | :--- |
| 1 | parents | categorical | Parents' occupation. |
| 2 | has_nurs | categorical | Employment of parents has nursery. |
| 3 | form | categorical | Form of the family. |
| 4 | children | categorical | Number of children in the family. |
| 5 | housing | categorical | Housing conditions. |
| 6 | finance | categorical | Financial standing of the family. |
| 7 | social | categorical | Social conditions. |
| 8 | health | categorical | Health conditions. |
| 9 | class | categorical | Evaluation of applications for nursery schools. |

### Parents

Unique values: 3.

| Value | Samples |
| :--- | :--- |
| great_pret | 4320 |
| pretentious | 4320 |
| usual | 4320 |

### Has nursery

Unique values: 5.

| Value | Samples |
| :--- | :--- |
| critical | 2592 |
| improper | 2592 |
| less_proper | 2592 |
| proper | 2592 |
| very_crit | 2592 |

### Form

Unique values: 4.

| Value | Samples |
| :--- | :--- |
| complete | 3240 |
| completed | 3240 |
| foster | 3240 |
| incomplete | 3240 |

### Children

Unique values: 4.

| Value | Samples |
| :--- | :--- |
| 1 | 3240 |
| 2 | 3240 |
| 3 | 3240 |
| more | 3240 |

### Housing

Unique values: 3.

| Value | Samples |
| :--- | :--- |
| convenient | 4320 |
| critical | 4320 |
| less_conv | 4320 |

### Finance

Unique values: 2.

| Value | Samples |
| :--- | :--- |
| convenient | 6480 |
| inconv | 6480 |

### Social

Unique values: 3.

| Value | Samples |
| :--- | :--- |
| nonprob | 4320 |
| problematic | 4320 |
| slightly_prob | 4320 |

### Health

Unique values: 3.

| Value | Samples |
| :--- | :--- |
| not_recom | 4320 |
| priority | 4320 |
| recommended | 4320 |

### Class

Unique values: 5.

| Value | Samples |
| :--- | :--- |
| not_recom | 4320 |
| recommend | 2 |
| very_recom | 328 |
| priority | 4266 |
| spec_prior | 4044 |