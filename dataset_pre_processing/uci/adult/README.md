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

| Value |
| --- |
| Private |
| Self-emp-not-inc |
| Self-emp-inc |
| Federal-gov |
| Local-gov |
| State-gov |
| Without-pay |
| Never-worked |

### Education

Unique values: 16.

| Value |
| --- |
| Bachelors |
| Some-college |
| 11th |
| HS-grad |
| Prof-school |
| Assoc-acdm |
| Assoc-voc |
| 9th |
| 7th-8th |
| 12th |
| Masters |
| 1st-4th |
| 10th |
| Doctorate |
| 5th-6th |
| Preschool |

### Marital status

Unique values: 7.

| Value |
| --- |
| Married-civ-spouse |
| Divorced |
| Never-married |
| Separated |
| Widowed |
| Married-spouse-absent |
| Married-AF-spouse |

### Occupation

Unique values: 14.

| Value |
| --- |
| Tech-support |
| Craft-repair |
| Other-service |
| Sales |
| Exec-managerial |
| Prof-specialty |
| Handlers-cleaners |
| Machine-op-inspct |
| Adm-clerical |
| Farming-fishing |
| Transport-moving |
| Priv-house-serv |
| Protective-serv |
| Armed-Forces |

### Relationship

Unique values: 6.

| Value |
| --- |
| Wife |
| Own-child |
| Husband |
| Not-in-family |
| Other-relative |
| Unmarried |

### Race

Unique values: 5.

| Value |
| --- |
| White |
| Asian-Pac-Islander |
| Amer-Indian-Eskimo |
| Other |
| Black |

### Sex

Unique values: 2.

| Value |
| --- |
| Female |
| Male |

### Native country

Unique values: 41.

| Value |
| --- |
| United-States |
| Cambodia |
| England |
| Puerto-Rico |
| Canada |
| Germany |
| Outlying-US(Guam-USVI-etc) |
| India |
| Japan |
| Greece |
| South |
| China |
| Cuba |
| Iran |
| Honduras |
| Philippines |
| Italy |
| Poland |
| Jamaica |
| Vietnam |
| Mexico |
| Portugal |
| Ireland |
| France |
| Dominican-Republic |
| Laos |
| Ecuador |
| Taiwan |
| Haiti |
| Columbia |
| Hungary |
| Guatemala |
| Nicaragua |
| Scotland |
| Thailand |
| Yugoslavia |
| El-Salvador |
| Trinadad&Tobago |
| Peru |
| Hong |
| Holand-Netherlands |

### Income

| Value |
| --- |
| >50K |
| <=50K |