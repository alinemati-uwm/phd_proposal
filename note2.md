
# Recommended *Best* Variables:

(For most analysis: prediction, survival, quality of care, cost analysis)

### 1. Patient Demographics

| Variable | Reason |
|----------|--------|
| AGE / AGEGROUP | Age group is useful for stratification |
| FEMALE | Sex variable |
| RACE | Demographic disparities |
| HISPANIC | Ethnicity |
| ZIPINC_QRTL | Socioeconomic status indicator (income quartile by ZIP) |

---

### 2. Admission Characteristics
| Variable | Reason |
|----------|--------|
| ATYPE | Admission type (urgent, elective, trauma) |
| ASOURCE | Source of admission (ER, clinic, transfer) |
| AWEEKEND | Weekend admission flag |
| TRAN_IN / TRAN_OUT | Transfer status |

---

### 3. Hospital Characteristics
| Variable | Reason |
|----------|--------|
| HOSPID | Hospital ID |
| HOSPST | State |
| PL_NCHS / PL_CBSA | Urban-Rural / Metro Area info |

---

### 4. Clinical Information
| Variable | Reason |
|----------|--------|
| DRG / DRGVER | Diagnosis-Related Group |
| MDC | Major Diagnostic Category |
| DXPOAn / I10_DXn | Diagnoses with POA flag |
| I10_INJURY / I10_INJURY_TYPEs | Injury indicators |
| I10_PROCTYPE | Procedure type |
| I10_ORPROC | Operating Room procedure indicator |
| PRDAYn / PRMONTHn / PRYEARn | Procedure timing |

---

### 5. Outcome & Resource Use
| Variable | Reason |
|----------|--------|
| DIED | Mortality indicator |
| LOS | Length of Stay |
| TOTCHG | Total hospital charges |
| READMIT | Readmission indicator |
| DISPUNIFORM | Discharge disposition |
| DAYSICU / DAYSCCU / DAYSNICU | ICU utilization |

---

### 6. Socioeconomic & Regional
| Variable | Reason |
|----------|--------|
| MEDINCSTQ | Median household income |
| ZIP | Geographical analysis |
| PL_RUCC / PL_UIC / PL_UR_CAT4 | Rural-Urban Classification |

