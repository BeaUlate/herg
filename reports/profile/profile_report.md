# CHEMBL240 (hERG) raw activity profile


## Overall shape

| quantity                      |     n |
|:------------------------------|------:|
| activity records              | 41078 |
| distinct assays               |  4829 |
| distinct compounds (molregno) | 26310 |
| distinct parent compounds     | 26093 |
| distinct InChIKeys            | 26254 |
| distinct documents            |  3494 |
| rows with no SMILES           |   102 |
| rows with no standard_value   | 10545 |
| rows with no pchembl_value    | 26815 |


## standard_type

| standard_type         |     n |   pct |
|:----------------------|------:|------:|
| IC50                  | 19130 | 46.57 |
| Inhibition            |  7808 | 19.01 |
| Ki                    |  3689 |  8.98 |
| kon                   |  2946 |  7.17 |
| k_off                 |  2946 |  7.17 |
| AC50                  |  1823 |  4.44 |
| Potency               |   679 |  1.65 |
| Activity              |   551 |  1.34 |
| EC50                  |   253 |  0.62 |
| delta pIC50 wt-mutant |   200 |  0.49 |
| INH                   |   197 |  0.48 |
| IC20                  |   164 |  0.4  |
| pIC50                 |   130 |  0.32 |
| IP                    |   112 |  0.27 |
| K                     |    92 |  0.22 |
| TIME                  |    50 |  0.12 |
| Kd                    |    47 |  0.11 |
| Ratio IC50            |    34 |  0.08 |
| IC25                  |    33 |  0.08 |
| pKi                   |    31 |  0.08 |
| Ratio                 |    31 |  0.08 |
| % Ctrl                |    29 |  0.07 |
| FC                    |    24 |  0.06 |
| Imax                  |    18 |  0.04 |
| Inflection point      |    13 |  0.03 |

*(showing 25 of 46 rows)*


## standard_type x standard_units

| standard_type         | standard_units   |     n |
|:----------------------|:-----------------|------:|
| IC50                  | nM               | 17099 |
| Inhibition            | %                |  7808 |
| kon                   | nan              |  2946 |
| k_off                 | s-1              |  2946 |
| Ki                    | nM               |  2741 |
| IC50                  | nan              |  2015 |
| AC50                  | nM               |  1823 |
| Ki                    | nan              |   948 |
| Potency               | nM               |   679 |
| EC50                  | nM               |   240 |
| Activity              | %                |   229 |
| delta pIC50 wt-mutant | nan              |   200 |
| INH                   | uM               |   157 |
| Activity              | nan              |   143 |
| IC20                  | uM               |   134 |
| pIC50                 | nan              |   130 |
| IP                    | nM               |   112 |
| Activity              | uM               |    96 |
| Activity              | nM               |    75 |
| TIME                  | hr               |    50 |
| Kd                    | nM               |    46 |
| K                     | /min             |    45 |
| INH                   | nM               |    39 |
| Ratio IC50            | nan              |    34 |
| IC25                  | uM               |    32 |

*(showing 25 of 69 rows)*


## standard_relation (censoring)

| standard_relation   |     n |   pct |
|:--------------------|------:|------:|
| =                   | 27879 | 67.87 |
| >                   |  7204 | 17.54 |
|                     |  5341 | 13    |
| <                   |   610 |  1.48 |
| <=                  |    22 |  0.05 |
| >=                  |    16 |  0.04 |
| ~                   |     6 |  0.01 |


## Censoring by endpoint type

| standard_type         |   (null) |   < |   <= |     = |    > |   >= |   ~ |   total |   pct_censored_or_null |
|:----------------------|---------:|----:|-----:|------:|-----:|-----:|----:|--------:|-----------------------:|
| IC50                  |     2022 | 290 |    4 | 12021 | 4773 |   16 |   4 |   19130 |                   37.2 |
| Inhibition            |     1331 | 226 |    2 |  6219 |   30 |    0 |   0 |    7808 |                   20.4 |
| Ki                    |      952 |  67 |    0 |  1815 |  855 |    0 |   0 |    3689 |                   50.8 |
| kon                   |        0 |   0 |    0 |  2946 |    0 |    0 |   0 |    2946 |                    0   |
| k_off                 |        0 |   0 |    0 |  2946 |    0 |    0 |   0 |    2946 |                    0   |
| AC50                  |        0 |   0 |    0 |   498 | 1325 |    0 |   0 |    1823 |                   72.7 |
| Potency               |      679 |   0 |    0 |     0 |    0 |    0 |   0 |     679 |                  100   |
| Activity              |      143 |   9 |   16 |   316 |   67 |    0 |   0 |     551 |                   42.6 |
| EC50                  |       13 |   6 |    0 |   203 |   30 |    0 |   1 |     253 |                   19.8 |
| delta pIC50 wt-mutant |        0 |   0 |    0 |   200 |    0 |    0 |   0 |     200 |                    0   |
| INH                   |        0 |   4 |    0 |   129 |   64 |    0 |   0 |     197 |                   34.5 |
| IC20                  |       26 |   8 |    0 |    95 |   35 |    0 |   0 |     164 |                   42.1 |
| pIC50                 |      129 |   0 |    0 |     1 |    0 |    0 |   0 |     130 |                   99.2 |
| IP                    |        0 |   0 |    0 |   107 |    5 |    0 |   0 |     112 |                    4.5 |
| K                     |        2 |   0 |    0 |    90 |    0 |    0 |   0 |      92 |                    2.2 |
| TIME                  |        0 |   0 |    0 |    50 |    0 |    0 |   0 |      50 |                    0   |
| Kd                    |        1 |   0 |    0 |    46 |    0 |    0 |   0 |      47 |                    2.1 |
| Ratio IC50            |        0 |   0 |    0 |    34 |    0 |    0 |   0 |      34 |                    0   |
| IC25                  |        0 |   0 |    0 |    23 |   10 |    0 |   0 |      33 |                   30.3 |
| pKi                   |       31 |   0 |    0 |     0 |    0 |    0 |   0 |      31 |                  100   |
| Ratio                 |        0 |   0 |    0 |    31 |    0 |    0 |   0 |      31 |                    0   |
| % Ctrl                |        0 |   0 |    0 |    29 |    0 |    0 |   0 |      29 |                    0   |
| FC                    |        0 |   0 |    0 |    19 |    5 |    0 |   0 |      24 |                   20.8 |
| Imax                  |        1 |   0 |    0 |    16 |    0 |    0 |   1 |      18 |                   11.1 |
| Inflection point      |        0 |   0 |    0 |    12 |    1 |    0 |   0 |      13 |                    7.7 |

*(showing 25 of 46 rows)*


## assay_type

| assay_type   |     n |   pct |
|:-------------|------:|------:|
| B            | 32640 | 79.46 |
| T            |  4390 | 10.69 |
| F            |  3597 |  8.76 |
| A            |   451 |  1.1  |


## confidence_score

|   confidence_score |     n |   pct |
|-------------------:|------:|------:|
|                  8 |  4913 | 11.96 |
|                  9 | 36165 | 88.04 |


## bao_format

| bao_format   |     n |   pct |
|:-------------|------:|------:|
| BAO_0000219  | 14480 | 35.25 |
| BAO_0000019  | 13121 | 31.94 |
| BAO_0000357  | 11213 | 27.3  |
| BAO_0000249  |  1961 |  4.77 |
| BAO_0000218  |   296 |  0.72 |
| BAO_0000221  |     7 |  0.02 |


## cell_name

| cell_name   |     n |   pct |
|:------------|------:|------:|
|             | 30977 | 75.41 |
| HEK293      |  7120 | 17.33 |
| CHO         |  2038 |  4.96 |
| CHO-K1      |   768 |  1.87 |
| Oocyte      |    37 |  0.09 |
| MCF7        |    37 |  0.09 |
| Sf9         |    32 |  0.08 |
| L929        |    29 |  0.07 |
| COS-7       |    24 |  0.06 |
| HEL         |    10 |  0.02 |
| HT-29       |     6 |  0.01 |


## assay_organism

| assay_organism         |     n |   pct |
|:-----------------------|------:|------:|
| Homo sapiens           | 36380 | 88.56 |
|                        |  4589 | 11.17 |
| Cricetulus griseus     |    77 |  0.19 |
| Cavia porcellus        |    26 |  0.06 |
| Canis lupus familiaris |     4 |  0.01 |
| Mustela putorius furo  |     1 |  0    |
| Blocker                |     1 |  0    |


## src_short_name (data source)

| src_short_name   |     n |   pct |
|:-----------------|------:|------:|
| LITERATURE       | 28126 | 68.47 |
| BINDINGDB        |  9210 | 22.42 |
| DRUGMATRIX       |  1742 |  4.24 |
| PUBCHEM_BIOASSAY |   803 |  1.95 |
| MMV_MBOX         |   800 |  1.95 |
| PATENT           |   287 |  0.7  |
| DONATED_PROBES   |    45 |  0.11 |
| ASAP             |    27 |  0.07 |
| LIT_EUBOPEN_CGL  |    12 |  0.03 |
| LIT_CHEM_PROBES  |    12 |  0.03 |
| FDA_APPROVAL     |     7 |  0.02 |
| SARS_COV_2       |     5 |  0.01 |
| OSM              |     2 |  0    |


## mutation (protein variant)

| mutation    |     n |   pct |
|:------------|------:|------:|
|             | 40820 | 99.37 |
| Y652A       |    42 |  0.1  |
| S624A       |    30 |  0.07 |
| T623S       |    25 |  0.06 |
| F656W       |    25 |  0.06 |
| F656M       |    25 |  0.06 |
| S624T       |    25 |  0.06 |
| Y652F       |    25 |  0.06 |
| F656T       |    25 |  0.06 |
| F656A       |    12 |  0.03 |
| L666A       |     4 |  0.01 |
| V659A       |     3 |  0.01 |
| F557L       |     3 |  0.01 |
| S631A       |     2 |  0    |
| L553A       |     2 |  0    |
| N658A       |     2 |  0    |
| Y667A       |     1 |  0    |
| I662A       |     1 |  0    |
| S620T,L666A |     1 |  0    |
| G628C,N588K |     1 |  0    |
| V549A       |     1 |  0    |
| L550A       |     1 |  0    |
| G628C,S631C |     1 |  0    |
| S631A,L666A |     1 |  0    |


## data_validity_comment

| data_validity_comment         |     n |   pct |
|:------------------------------|------:|------:|
|                               | 40596 | 98.83 |
| Outside typical range         |   473 |  1.15 |
| Potential transcription error |     8 |  0.02 |
| Potential author error        |     1 |  0    |


## potential_duplicate

|   potential_duplicate |     n |   pct |
|----------------------:|------:|------:|
|                     0 | 38855 | 94.59 |
|                     1 |  2223 |  5.41 |


## activity_comment

| activity_comment                                                                                                              |     n |   pct |
|:------------------------------------------------------------------------------------------------------------------------------|------:|------:|
|                                                                                                                               | 25154 | 61.23 |
| Not Determined                                                                                                                |  1874 |  4.56 |
| Summarised AC50 (mean value for measurements with a relation sign "="; largest value for measurements with relation sign ">") |  1822 |  4.44 |
| Inhibition < 50% @ 10 uM and thus dose-reponse curve not measured                                                             |  1670 |  4.07 |
| inconclusive                                                                                                                  |   372 |  0.91 |
| active                                                                                                                        |   281 |  0.68 |
| Active                                                                                                                        |   231 |  0.56 |
| Inactive                                                                                                                      |   186 |  0.45 |
| Weakly active                                                                                                                 |    69 |  0.17 |
| Not Active                                                                                                                    |    46 |  0.11 |
| ND                                                                                                                            |    35 |  0.09 |
| inactive                                                                                                                      |    32 |  0.08 |
| Highly active                                                                                                                 |    29 |  0.07 |
| NA                                                                                                                            |    19 |  0.05 |
| Dose-dependent effect                                                                                                         |    12 |  0.03 |
| Nd(Insoluble)                                                                                                                 |    12 |  0.03 |
| At Top Concentration                                                                                                          |     7 |  0.02 |
| Non-Toxic                                                                                                                     |     4 |  0.01 |
| 340971                                                                                                                        |     4 |  0.01 |
| 340970                                                                                                                        |     4 |  0.01 |
| 340969                                                                                                                        |     4 |  0.01 |
| 616513                                                                                                                        |     3 |  0.01 |
| 792959                                                                                                                        |     3 |  0.01 |
| 887432                                                                                                                        |     3 |  0.01 |
| 955372                                                                                                                        |     3 |  0.01 |

*(showing 25 of 3344 rows)*


## Records per year

|   year |   n_activities |   n_assays |   n_docs |
|-------:|---------------:|-----------:|---------:|
|     -1 |           3354 |         15 |        5 |
|   1995 |              7 |          2 |        1 |
|   1997 |             17 |          4 |        1 |
|   2001 |             48 |          6 |        4 |
|   2002 |            101 |         13 |        4 |
|   2003 |            124 |          6 |        5 |
|   2004 |            176 |         15 |       11 |
|   2005 |            177 |         22 |       14 |
|   2006 |            544 |         80 |       58 |
|   2007 |            758 |        125 |       61 |
|   2008 |           1015 |        103 |       95 |
|   2009 |           1988 |        189 |      141 |
|   2010 |           1725 |        225 |      165 |
|   2011 |           2201 |        314 |      206 |
|   2012 |           2110 |        325 |      234 |
|   2013 |           1412 |        237 |      171 |
|   2014 |           1186 |        316 |      163 |
|   2015 |           1707 |        235 |      160 |
|   2016 |           1750 |        270 |      209 |
|   2017 |           2657 |        261 |      192 |
|   2018 |           2759 |        240 |      190 |
|   2019 |           3794 |        240 |      188 |
|   2020 |           2799 |        270 |      217 |
|   2021 |           1917 |        326 |      248 |
|   2022 |           1577 |        262 |      204 |
|   2023 |           3445 |        249 |      188 |
|   2024 |           1123 |        320 |      230 |
|   2025 |            607 |        162 |      129 |


## doc_type

| doc_type    |     n |   pct |
|:------------|------:|------:|
| PUBLICATION | 28138 | 68.5  |
| PATENT      |  9497 | 23.12 |
| DATASET     |  3443 |  8.38 |


## journal

| journal                     |     n |   pct |
|:----------------------------|------:|------:|
|                             | 12935 | 31.49 |
| J Med Chem                  | 10640 | 25.9  |
| Bioorg Med Chem Lett        |  9501 | 23.13 |
| ACS Med Chem Lett           |  2048 |  4.99 |
| Eur J Med Chem              |  1851 |  4.51 |
| Nat Commun                  |  1823 |  4.44 |
| Bioorg Med Chem             |  1430 |  3.48 |
| Medchemcomm                 |   368 |  0.9  |
| J Nat Prod                  |   166 |  0.4  |
| RSC Med Chem                |   120 |  0.29 |
| J Pharmacol Toxicol Methods |    94 |  0.23 |
| Proc Natl Acad Sci U S A    |    38 |  0.09 |
| Cardiovasc Res              |    31 |  0.08 |
| Nature                      |    13 |  0.03 |
| Chem Biol Drug Des          |    11 |  0.03 |
| Science                     |     4 |  0.01 |
| Cancer Cell                 |     2 |  0    |
| Antimicrob Agents Chemother |     1 |  0    |
| Med Chem Res                |     1 |  0    |
| ChemMedChem                 |     1 |  0    |


## Records per assay

| stat   |      value |
|:-------|-----------:|
| count  | 4829       |
| mean   |    8.50652 |
| std    |   50.8741  |
| min    |    1       |
| 25%    |    1       |
| 50%    |    2       |
| 75%    |    6       |
| max    | 1822       |


Largest assays:

| assay_chembl_id   |   n_records |   n_compounds | types          |   year |   confidence_score | cell_name   |
|:------------------|------------:|--------------:|:---------------|-------:|-------------------:|:------------|
| CHEMBL5291828     |        1822 |          1804 | AC50           |   2023 |                  8 |             |
| CHEMBL1909190     |        1742 |           871 | IC50|Ki        |    nan |                  8 | HEK293      |
| CHEMBL5732052     |        1344 |           321 | Ki|k_off|kon   |   2019 |                  9 |             |
| CHEMBL5732504     |        1344 |           322 | Ki|k_off|kon   |   2017 |                  9 |             |
| CHEMBL1794573     |         679 |           661 | Potency        |    nan |                  8 |             |
| CHEMBL3301459     |         400 |           400 | Inhibition     |    nan |                  9 |             |
| CHEMBL3301460     |         400 |           400 | Inhibition     |    nan |                  9 |             |
| CHEMBL5735028     |         381 |           125 | IC50|k_off|kon |   2020 |                  9 |             |
| CHEMBL5737036     |         381 |           125 | IC50|k_off|kon |   2021 |                  9 |             |
| CHEMBL5733101     |         381 |           126 | IC50|k_off|kon |   2019 |                  9 |             |
| CHEMBL5734036     |         348 |           114 | IC50|k_off|kon |   2019 |                  9 |             |
| CHEMBL5733977     |         348 |           116 | IC50|k_off|kon |   2018 |                  9 |             |
| CHEMBL5733769     |         348 |           108 | IC50|k_off|kon |   2018 |                  9 |             |
| CHEMBL5731865     |         309 |           102 | IC50|k_off|kon |   2018 |                  9 |             |
| CHEMBL5739235     |         297 |            99 | IC50|k_off|kon |   2023 |                  9 |             |


## Records per compound

| stat   |       value |
|:-------|------------:|
| count  | 26310       |
| mean   |     1.56131 |
| std    |     1.73772 |
| min    |     1       |
| 25%    |     1       |
| 50%    |     1       |
| 75%    |     1       |
| max    |    67       |


## Replicate structure (the raw material for the variance analysis)

| quantity                                    |     n |
|:--------------------------------------------|------:|
| compounds with 1 record                     | 20207 |
| compounds with >= 2 records                 |  6103 |
| compounds with >= 3 records                 |  2992 |
| compounds with >= 2 distinct documents      |  2478 |
| compounds with >= 2 distinct standard_types |  4077 |


Most-measured compounds:

|   molregno |   n_records |   n_assays |   n_docs |   n_types | pref_name     | inchikey                    |
|-----------:|------------:|-----------:|---------:|----------:|:--------------|:----------------------------|
|     557741 |          67 |         61 |       48 |         8 | CISAPRIDE     | DCSUBABJRXZOMT-UHFFFAOYSA-N |
|      19569 |          41 |         38 |       34 |         6 | TERFENADINE   | GUGOEEXESWIERI-UHFFFAOYSA-N |
|     428371 |          38 |         38 |        1 |         3 |               | VWNMWKSURFWKAL-HXOBKFHXSA-N |
|      65605 |          38 |         34 |       31 |         6 | ASTEMIZOLE    | GXDALQBWZGODGZ-UHFFFAOYSA-N |
|       1219 |          33 |         32 |       27 |         4 | VERAPAMIL     | SGTNSNPWRIOYBX-UHFFFAOYSA-N |
|       5638 |          32 |         30 |       23 |         8 | DOFETILIDE    | IXTMWRCNAAVVAI-UHFFFAOYSA-N |
|     121485 |          32 |         32 |       32 |         2 | REL-CISAPRIDE | DCSUBABJRXZOMT-RBBKRZOGSA-N |
|    2998991 |          30 |          2 |        2 |         3 |               | PCPCDRDQIBENHU-UHFFFAOYSA-N |
|    2985115 |          30 |          2 |        2 |         3 |               | MOWXJLUYGFNTAL-UHFFFAOYSA-N |
|     152611 |          27 |         27 |       24 |         3 |               | SRUISGSHWFJION-UHFFFAOYSA-N |
|    3223711 |          27 |          9 |        8 |         3 |               | GXJBVCKDEHELEL-UHFFFAOYSA-N |
|    3143852 |          24 |          2 |        2 |         3 |               | JEOIEFCSPPXNAG-UHFFFAOYSA-N |
|       7714 |          24 |         22 |       22 |         4 | RISPERIDONE   | RAPZEAPATHNIPO-UHFFFAOYSA-N |
|    1448253 |          24 |         22 |        1 |         5 | DARUISOLINE   | BURJAQFYNVMZDV-FIRIVFDPSA-N |
|    3194883 |          24 |          2 |        2 |         3 |               | YNJIBQSLMOPTQF-UHFFFAOYSA-N |


## IC50 value distribution (nM, unfiltered)

|   quantile |         nM |   pIC50 |
|-----------:|-----------:|--------:|
|       0    |      0.021 |   10.68 |
|       0.01 |      3.697 |    8.43 |
|       0.05 |     56     |    7.25 |
|       0.25 |   2400     |    5.62 |
|       0.5  |  10000     |    5    |
|       0.75 |  30000     |    4.52 |
|       0.95 |  90000     |    4.05 |
|       0.99 | 300000     |    3.52 |
|       1    |      1e+09 |    0    |


## IC50 edge cases

| quantity                                 |     n |
|:-----------------------------------------|------:|
| IC50 rows                                | 17114 |
| IC50 rows in nM                          | 17098 |
| IC50 rows in other/blank units           |    16 |
| IC50 < 0.1 nM (implausible, check units) |     2 |
| IC50 > 1 mM (implausible, check units)   |    88 |
| IC50 rows censored (relation != '=')     |  5093 |
| IC50 rows with a validity comment        |   378 |
| IC50 rows with no pchembl_value          |  5405 |


## Keyword reconnaissance over assay descriptions (assay level, probes overlap)

| keyword_probe               |   n_assays |   pct_of_assays |
|:----------------------------|-----------:|----------------:|
| patch clamp                 |       1713 |            35.5 |
| HEK                         |        947 |            19.6 |
| binding/radioligand         |        793 |            16.4 |
| CHO                         |        694 |            14.4 |
| whole-cell                  |        431 |             8.9 |
| automated                   |        366 |             7.6 |
| holding/step voltage stated |        360 |             7.5 |
| flux/fluorescence           |        273 |             5.7 |
| manual                      |        167 |             3.5 |
| QPatch                      |        152 |             3.1 |
| IonWorks                    |        141 |             2.9 |
| oocyte                      |         51 |             1.1 |
| temperature stated          |         44 |             0.9 |
| PatchXpress                 |         26 |             0.5 |
| SyncroPatch|Qube|Patchliner |         15 |             0.3 |


200 randomly sampled assay descriptions written to `24_description_sample_200.csv` — this is the file to read by hand before writing the method classifier.
