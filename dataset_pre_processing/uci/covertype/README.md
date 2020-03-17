# Covertype

Forest cover type.
[[Source]](https://archive.ics.uci.edu/ml/datasets/Covertype)

## Samples

Number of samples: 581,012.

No missing values.

## Variables

| Numerical | Categorical | Binary | Total |
| :--- | :--- | :--- | :--- |
| 10 | 1 | 44 | 55 |

| Predictive | Non-Predictive | Target | Total |
| :--- | :--- | :--- | :--- |
| 54 | 0 | 1 | 55 |

The variable index corresponds to the order in the original data.

The corresponding feature index after the transformation may differ (check the metadata).

The binary variables are the result of one-hot-encoding two different categorical variables.

The categorical variables are encoded with integers.

The target variable is "Cover_Type".

| Index | Name | Type (Unit) | Description |
| --- | --- | --- | --- |
| 1 | Elevation | numerical (meters) | Elevation. |
| 2 | Aspect | numerical (degrees azimuth) | Aspect. |
| 3 | Slope | numerical (degrees) | Slope. |
| 4 | Horizontal_Distance_To_Hydrology | numerical (meters) | Horizontal distance to nearest surface water features. |
| 5 | Vertical_Distance_To_Hydrology | numerical (meters) | Vertical distance to nearest surface water features. |
| 6 | Horizontal_Distance_To_Roadways | numerical (meters) | Horizontal distance to nearest roadway. |
| 7 | Hillshade_9am | numerical (0 to 255 index) | Hillshade index at 9am, summer solstice. |
| 8 | Hillshade_Noon | numerical (0 to 255 index) | Hillshade index at noon, summer solstice. |
| 9 | Hillshade_3pm | numerical (0 to 255 index) | Hillshade index at 3pm, summer solstice. |
| 10 | Horizontal_Distance_To_Fire_Points | numerical (meters) | Horizontal distance to nearest wildfire ignition points. |
| 11 - 14 | Wilderness_Area | binary | Wilderness area designation. |
| 15 - 54 | Soil_Type | binary | Soil type designation. |
| 55 | Cover_Type | categorical | Forest Cover Type designation |

### Wilderness Area

Unique values: 4.

The variable number of these binary variables can be calculated with `11 + ID - 1`: 

| ID | Description |
| --- | --- |
| 1 | Rawah Wilderness Area |
| 2 | Neota Wilderness Area |
| 3 | Comanche Peak Wilderness Area |
| 4 | Cache la Poudre Wilderness Area |

### Soil Type

Unique values: 40.

The variable number of these binary variables can be calculated with `15 + ID - 1`:

| ID | USFS/ELU* | Description |
| --- | --- | --- |
 1 | 2702 | Cathedral family - Rock outcrop complex, extremely stony |
 2 | 2703 | Vanet - Ratake families complex, very stony |
 3 | 2704 | Haploborolis - Rock outcrop complex, rubbly |
 4 | 2705 | Ratake family - Rock outcrop complex, rubbly |
 5 | 2706 | Vanet family - Rock outcrop complex complex, rubbly |
 6 | 2717 | Vanet - Wetmore families - Rock outcrop complex, stony |
 7 | 3501 | Gothic family |
 8 | 3502 | Supervisor - Limber families complex |
 9 | 4201 | Troutville family, very stony |
10 | 4703 | Bullwark - Catamount families - Rock outcrop complex, rubbly |
11 | 4704 | Bullwark - Catamount families - Rock land complex, rubbly |
12 | 4744 | Legault family - Rock land complex, stony |
13 | 4758 | Catamount family - Rock land - Bullwark family complex, rubbly |
14 | 5101 | Pachic Argiborolis - Aquolis complex |
15 | 5151 | unspecified in the USFS Soil and ELU Survey |
16 | 6101 | Cryaquolis - Cryoborolis complex |
17 | 6102 | Gateview family - Cryaquolis complex |
18 | 6731 | Rogert family, very stony |
19 | 7101 | Typic Cryaquolis - Borohemists complex |
20 | 7102 | Typic Cryaquepts - Typic Cryaquolls complex |
21 | 7103 | Typic Cryaquolls - Leighcan family, till substratum complex |
22 | 7201 | Leighcan family, till substratum, extremely bouldery |
23 | 7202 | Leighcan family, till substratum - Typic Cryaquolls complex |
24 | 7700 | Leighcan family, extremely stony |
25 | 7701 | Leighcan family, warm, extremely stony |
26 | 7702 | Granile - Catamount families complex, very stony |
27 | 7709 | Leighcan family, warm - Rock outcrop complex, extremely stony |
28 | 7710 | Leighcan family - Rock outcrop complex, extremely stony |
29 | 7745 | Como - Legault families complex, extremely stony |
30 | 7746 | Como family - Rock land - Legault family complex, extremely stony |
31 | 7755 | Leighcan - Catamount families complex, extremely stony |
32 | 7756 | Catamount family - Rock outcrop - Leighcan family complex, extremely stony |
33 | 7757 | Leighcan - Catamount families - Rock outcrop complex, extremely stony |
34 | 7790 | Cryorthents - Rock land complex, extremely stony |
35 | 8703 | Cryumbrepts - Rock outcrop - Cryaquepts complex |
36 | 8707 | Bross family - Rock land - Cryumbrepts complex, extremely stony |
37 | 8708 | Rock outcrop - Cryumbrepts - Cryorthents complex, extremely stony |
38 | 8771 | Leighcan - Moran families - Cryaquolls complex, extremely stony |
39 | 8772 | Moran family - Cryorthents - Leighcan family complex, extremely stony |
40 | 8776 | Moran family - Cryorthents - Rock land complex, extremely stony |

(*) USFS/ELU is formed by the two most/least significant digits respectively.

### Cover Type

Unique values: 7.

| Class | Samples |
| :--- | ---: |
| Spruce-Fir | 211840 |
| Lodgepole Pine | 283301 | 
| Ponderosa Pine | 35754 |
| Cottonwood/Willow | 2747 |
| Aspen | 9493 |
| Douglas-fir | 17367 | 
| Krummholz | 20510 |