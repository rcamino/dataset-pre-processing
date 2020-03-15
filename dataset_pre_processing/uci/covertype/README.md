# Covertype

Source: https://archive.ics.uci.edu/ml/datasets/Covertype

Forest cover type.

## Samples

Number of samples: 581,012.

No missing values.

## Variables

| Numerical | Binary | Total |
| :--- | :--- | :--- |
| 10 | 44 | 54 |

| Name | Data Type | Measurement | Description |
| --- | --- | --- | --- |
| Elevation | numerical | meters | Elevation in meters |
| Aspect | numerical | azimuth | Aspect in degrees azimuth |
| Slope | numerical | degrees | Slope in degrees |
| Horizontal_Distance_To_Hydrology | numerical | meters | Horz Dist to nearest surface water features |
| Vertical_Distance_To_Hydrology | numerical | meters | Vert Dist to nearest surface water features |
| Horizontal_Distance_To_Roadways | numerical | meters | Horz Dist to nearest roadway |
| Hillshade_9am | numerical | 0 to 255 index | Hillshade index at 9am, summer solstice |
| Hillshade_Noon | numerical | 0 to 255 index | Hillshade index at noon, summer soltice |
| Hillshade_3pm | numerical | 0 to 255 index | Hillshade index at 3pm, summer solstice |
| Horizontal_Distance_To_Fire_Points | numerical | meters | Horz Dist to nearest wildfire ignition points |
| Wilderness_Area (4 binary columns) | binary | 0 (absence) or 1 (presence) | Wilderness area designation |
| Soil_Type (40 binary columns) | binary | 0 (absence) or 1 (presence) | Soil Type designation |

Wilderness Areas:

| ID | Wilderness Area |
| --- | --- |
| 1 | Rawah Wilderness Area |
| 2 | Neota Wilderness Area |
| 3 | Comanche Peak Wilderness Area |
| 4 | Cache la Poudre Wilderness Area |

Soil Types:

| Study | USFS/ELU* | Description |
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

## Target Variable

The target variable is the "Forest Cover Type designation" (7 classes):

| Class | Samples |
| :--- | ---: |
| Spruce-Fir | 211840 |
| Lodgepole Pine | 283301 | 
| Ponderosa Pine | 35754 |
| Cottonwood/Willow | 2747 |
| Aspen | 9493 |
| Douglas-fir | 17367 | 
| Krummholz | 20510 |
| Total | 581012