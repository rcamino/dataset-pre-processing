# Adult

Predict whether income exceeds $50K/yr based on census data.
[[Source]](http://archive.ics.uci.edu/ml/datasets/adult)

**WARNING**: Also known as "[Census Income](http://archive.ics.uci.edu/ml/datasets/Census+Income)"!

## Samples

The data is originally split into train and test and has some missing values:

| | Train | Test | Total |
| :--- | :--- | :--- | :--- |
| With Missing | 32561 | 16281 | 48842 |
| Without Missing | 30162 | 15060 | 45222 |

## Variables

| Numerical | Categorical | Binary | Total |
| :--- | :--- | :--- | :--- |
| 6 | 9 | 0 | 15 |

| Predictive | Non-Predictive | Target | Total |
| :--- | :--- | :--- | :--- |
| 14 | 0 | 1 | 15 |

The only descriptions we have for the variables is their names.

The variable index corresponds to the order in the original data.

The corresponding feature index after the transformation may differ (check the metadata).

The categorical variables are not encoded.

The target variable is "income".

| Index | Name | Type |
| --- | --- | --- |
| 1 | age | numerical |
| 2 | workclass | categorical |
| 3 | fnlwgt | numerical |
| 4 | education | categorical |
| 5 | education-num | numerical |
| 6 | marital-status | categorical |
| 7 | occupation | categorical |
| 8 | relationship | categorical |
| 9 | race | categorical |
| 10 | sex | categorical |
| 11 | capital-gain | numerical |
| 12 | capital-loss | numerical |
| 13 | hours-per-week | numerical |
| 14 | native-country | categorical |
| 15 | income | categorical |

### Workclass

Unique values: 8.

| Value | Samples |
| :--- | :--- |
| Federal-gov | 1406 |
| Local-gov | 3100 |
| Never-worked | 0 |
| Private | 33307 |
| Self-emp-inc | 1646 |
| Self-emp-not-inc | 3796 |
| State-gov | 1946 |
| Without-pay | 21 |

### Education

Unique values: 16.

| Value | Samples |
| :--- | :--- |
| 10th | 1223 |
| 11th | 1619 |
| 12th | 577 |
| 1st-4th | 222 |
| 5th-6th | 449 |
| 7th-8th | 823 |
| 9th | 676 |
| Assoc-acdm | 1507 |
| Assoc-voc | 1959 |
| Bachelors | 7570 |
| Doctorate | 544 |
| HS-grad | 14783 |
| Masters | 2514 |
| Preschool | 72 |
| Prof-school | 785 |
| Some-college | 9899 |

### Marital status

Unique values: 7.

| Value | Samples |
| :--- | :--- |
| Divorced | 6297 |
| Married-AF-spouse | 32 |
| Married-civ-spouse | 21055 |
| Married-spouse-absent | 552 |
| Never-married | 14598 |
| Separated | 1411 |
| Widowed | 1277 |

### Occupation

Unique values: 14.

| Value | Samples |
| :--- | :--- |
| Adm-clerical | 5540 |
| Armed-Forces | 14 |
| Craft-repair | 6020 |
| Exec-managerial | 5984 |
| Farming-fishing | 1480 |
| Handlers-cleaners | 2046 |
| Machine-op-inspct | 2970 |
| Other-service | 4808 |
| Priv-house-serv | 232 |
| Prof-specialty | 6008 |
| Protective-serv | 976 |
| Sales | 5408 |
| Tech-support | 1420 |
| Transport-moving | 2316 |

### Relationship

Unique values: 6.

| Value | Samples |
| :--- | :--- |
| Husband | 18666 |
| Not-in-family | 11702 |
| Other-relative | 1349 |
| Own-child | 6626 |
| Unmarried | 4788 |
| Wife | 2091 |

### Race

Unique values: 5.

| Value | Samples |
| :--- | :--- |
| Amer-Indian-Eskimo | 435 |
| Asian-Pac-Islander | 1303 |
| Black | 4228 |
| Other | 353 |
| White | 38903 |

### Sex

Unique values: 2.

| Value | Samples |
| :--- | :--- |
| Female | 14695 |
| Male | 30527 |

### Native country

Unique values: 41.

| Value | Samples |
| :--- | :--- |
| Cambodia | 26 |
| Canada | 163 |
| China | 113 |
| Columbia | 82 |
| Cuba | 133 |
| Dominican-Republic | 97 |
| Ecuador | 43 |
| El-Salvador | 147 |
| England | 119 |
| France | 36 |
| Germany | 193 |
| Greece | 49 |
| Guatemala | 86 |
| Haiti | 69 |
| Holand-Netherlands | 1 |
| Honduras | 19 |
| Hong | 28 |
| Hungary | 18 |
| India | 147 |
| Iran | 56 |
| Ireland | 36 |
| Italy | 100 |
| Jamaica | 103 |
| Japan | 89 |
| Laos | 21 |
| Mexico | 903 |
| Nicaragua | 48 |
| Outlying-US(Guam-USVI-etc) | 22 |
| Peru | 45 |
| Philippines | 283 |
| Poland | 81 |
| Portugal | 62 |
| Puerto-Rico | 175 |
| Scotland | 20 |
| South | 101 |
| Taiwan | 55 |
| Thailand | 29 |
| Trinadad&Tobago | 26 |
| United-States | 41292 |
| Vietnam | 83 |
| Yugoslavia | 23 |


### Income

Unique values: 2.

| Value | Samples |
| :--- | :--- |
| <=50K | 34014 |
| >50K | 11208 |