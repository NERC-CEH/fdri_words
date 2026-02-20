# Biomet Data for FDRI Eddy Covariance

## Overview

Biomet (biometric/meteorological) data provides essential ancillary measurements for eddy covariance flux processing. This document defines sources, formats, and transformations.

---

## Data Source

**File format:** CSV with header rows  
**Frequency:** 30-minute intervals  
**Delivery:** TBD 
**Sites:** PLYNL, BICKL, etc.

---

## Key Variables

| Variable | Description | Units |
|----------|-------------|-------|
| TIMESTAMP_1 | Timestamp | yyyy-mm-dd HH:MM |
| Ta_1_1_1 | Air temperature | °C |
| RH_1_1_1 | Relative humidity | % |
| Pa_1_1_1 | Air pressure | kPa |
| SHF_1_1_1 | Soil heat flux (sensor 1) | W m⁻² |
| SHF_2_1_1 | Soil heat flux (sensor 2) | W m⁻² |
| Rn_1_1_1 | Net radiation | W m⁻² |
| SWin_1_1_1 | Shortwave incoming radiation | W m⁻² |

---

## Format

**Input (CSV):**
```csv
TIMESTAMP_1,Ta_1_1_1,RH_1_1_1,Pa_1_1_1,SHF_1_1_1,SHF_2_1_1,Rn_1_1_1,SWin_1_1_1
yyyy-mm-dd HH:MM,C,%,kPa,W m-2,W m-2,W m-2,W m-2
2014-11-05 12:30:00,6.503,76.18,-9999,10.10544,2.26121,119.59,270
2014-11-05 13:00:00,6.131,71.1,-9999,10.41839,2.67129,68.24,186.2
```

**Missing data:** `-9999`

---

## Transformations

### Variable Mapping for EddyPro

| Biomet CSV Name | EddyPro/AmeriFlux Name |
|-----------------|------------------------|
| Ta_1_1_1 | TA |
| RH_1_1_1 | RH |
| Pa_1_1_1 | PA |
| SHF_1_1_1 | G_1 |
| SHF_2_1_1 | G_2 |
| Rn_1_1_1 | NETRAD |
| SWin_1_1_1 | SW_IN |

### Unit Conversions

**None required** - All variables already in standard units:
- Ta: °C
- RH: %
- Pa: kPa
- SHF: W m⁻²
- Rn: W m⁻²
- SWin: W m⁻²

### Timestamp Conversion

**Input:** `yyyy-mm-dd HH:MM` (e.g., `2014-11-05 12:30:00`)  
**Output:** ISO 8601 UTC (e.g., `2014-11-05T12:30:00Z`)

### Quality Control

- **Missing data:** `-9999` (replace with standard missing value)
- **Range checks:**
  - Ta: Flag if <-40°C or >50°C
  - RH: Flag if <0% or >100%
  - Pa: Flag if <50 kPa or >110 kPa
  - SHF: Flag if <-200 or >200 W m⁻²
  - Rn: Flag if <-200 or >1000 W m⁻²
  - SWin: Flag if <0 or >1500 W m⁻²

---

## Storage

**S3 path:**
```
s3://flux-data/flux/ancillary/biomet/
└── site=PLYNL/date=2024/
    └── data.csv
```

---

## References
- EddyPro documentation: Biomet file requirements