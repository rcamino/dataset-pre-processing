# Default of credit card clients

Source: https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients

Default of credit card clients in Taiwan.

## Samples

Number of samples: 30,000.

## Variables

| Numerical | Categorical | Binary | Total |
| :--- | :--- | :--- | :--- |
| 15 | 9 | 1 | 25 |

| Predictive | Non-Predictive | Target | Total |
| :--- | :--- | :--- | :--- |
| 23 | 1 | 1 | 25 |

The variable index corresponds to the order in the original data.

The corresponding feature index after the transformation may differ (check the metadata).

The categorical variables are encoded with integers.

The "ID" variable is ignored.

The target variable is "default payment next month".

| Index | Name | Type (Unit) | Description |
| :--- | :--- | :--- | :--- |
1 | ID | numerical | Case identifier. |
2 | LIMIT_BAL | numerical (NT dollar) | Amount of the given credit: it includes both the individual consumer credit and his/her family (supplementary) credit. |
3 | SEX | categorical | Gender. |
4 | EDUCATION | categorical | Education. |
5 | MARRIAGE | categorical | Marital status. |
6 | AGE | numerical (years) | Age. |
7 | PAY_0* | categorical | repayment status in September, 2005. |
8 | PAY_2 | categorical | repayment status in August, 2005. |
... |
12 | PAY_6 | categorical | repayment status in April, 2005. |
13 | BILL_AMT1 | numerical (NT dollar) | amount of bill statement in September, 2005. |
14 | BILL_AMT2 | numerical (NT dollar) | amount of bill statement in August, 2005. |
... |
18 | BILL_AMT6 | numerical (NT dollar) | amount of bill statement in April, 2005. |
19 | PAY_AMT1 | numerical (NT dollar) | amount paid in September, 2005. |
20 | PAY_AMT2 | numerical (NT dollar) | amount paid in August, 2005. |
... |
24 | PAY_AMT6 | numerical (NT dollar) | amount paid in April, 2005. |
25 | default payment next month | binary | indicates if the client defaults in the following month |

(*) For some reason PAY_ has starts from index 0 but skips index 1.

### Gender

Unique values: 2.

| Value | Description |
| --- | --- |
| 1 | male |
| 2 | female |

### Education

Unique values: 7.

The description on the UCI repository has information for values in the range \[1, 4],
but the data presents values in the range \[0, 6].

Additional information was taken from this [Kaggle discussion](https://www.kaggle.com/uciml/default-of-credit-card-clients-dataset/discussion/34608).

| Value | Description |
| --- | --- |
| 0 | others |
| 1 | graduate school |
| 2 | university |
| 3 | high school |
| 4 | others |
| 5 | others |
| 6 | others |

We merge all the "others" together.

### Marital status

Unique values: 4.

The description on the UCI repository has information for values in the range \[1, 3],
but the data presents values in the range \[0, 3].

Additional information was taken from this [Kaggle discussion](https://www.kaggle.com/uciml/default-of-credit-card-clients-dataset/discussion/34608).

| Value | Description |
| --- | --- |
| 0 | others |
| 1 | married |
| 2 | single |
| 3 | divorce |

### Repayment status (any of them)

Unique values: 12.

The description on the UCI repository has no information for values -2 and 0.

Additional information was taken from this [Kaggle discussion](https://www.kaggle.com/uciml/default-of-credit-card-clients-dataset/discussion/34608).

Also it seems that the value for -1 was wrong.

| Value | Description |
| --- | --- |
| -2 | no consumption |
| -1 | paid in full |
| 0 | use of revolving credit |
| 1 | payment delay for one month |
| 2 | payment delay for one month |
| 3 | payment delay for two months |
| 4 | payment delay for three months |
| 5 | payment delay for four months |
| 6 | payment delay for five months |
| 7 | payment delay for six months |
| 8 | payment delay for eight months |
| 9 | payment delay for nine months and above |

## Target Variable

Default payment in next month: Yes = 1, No = 0.