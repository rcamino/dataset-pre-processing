# Nursery

Source: https://archive.ics.uci.edu/ml/datasets/Nursery

Nursery Database was derived from a hierarchical decision model originally developed to rank applications for nursery schools.

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

| Value |
| --- |
| usual |
| pretentious |
| great_pret |

### Has nursery

Unique values: 5.

| Value |
| --- |
| proper |
| less_proper |
| improper |
| critical |
| very_crit |

### Form

Unique values: 4.

| Value |
| --- |
| complete |
| completed |
| incomplete |
| foster |

### Children

Unique values: 4.

| Value |
| --- |
| 1 |
| 2 |
| 3 |
| more |

### Housing

Unique values: 3.

| Value |
| --- |
| convenient |
| less_conv |
| critical |

### Finance

Unique values: 2.

| Value |
| --- |
| convenient |
| inconv |

### Social

Unique values: 3.

| Value |
| --- |
| nonprob |
| slightly_prob |
| problematic |

### Health

Unique values: 3.

| Value |
| --- |
| recommended |
| priority |
| not_recom |

## Class distribution

| Value | Samples |
| :--- | :--- |
| not_recom | 4320 |
| recommend | 2 |
| very_recom | 328 |
| priority | 4266 |
| spec_prior | 4044 |