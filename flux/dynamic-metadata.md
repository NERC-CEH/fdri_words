# Dynamic Metadata for FDRI Eddy Covariance

## Overview

Dynamic metadata captures time-varying site characteristics essential for eddy covariance flux processing. This document defines sources, formats, and transformations.

---

## Data Source

**File format:** Text file (.txt) with CSV structure and header row  
**Frequency:** Variable (updated when values change, typically monthly)  
**Delivery:** TBD  
**Sites:** PLYNL, BICKL, etc.

---

## Key Variables

| Variable | Description | Units |
|----------|-------------|-------|
| date | Date of change | yyyy-mm-dd |
| time | Time of change | HH:MM |
| canopy_height | Vegetation canopy height | m |

---

## Format

**Input (.txt file with CSV structure):**
```
date,time,canopy_height
2014-11-05,12:30,0.06
2014-12-01,12:00,0.05
2015-01-01,12:00,0.05
2015-02-01,12:00,0.05
2015-03-01,12:00,0.05
2015-04-01,12:00,0.07
```

**Missing data:** Not applicable (only records when values change)

---

## Transformations

### Variable Mapping for EddyPro

| CSV Name | EddyPro Name | Notes |
|----------|--------------|-------|
| canopy_height | canopy_height | Used for footprint calculations |

### Unit Conversions

**None required** - Already in standard units:
- canopy_height: meters (m)

### Timestamp Conversion

**Input:** Separate `date` (yyyy-mm-dd) and `time` (HH:MM) columns  
**Output:** Combined ISO 8601 UTC (e.g., `2014-11-05T12:30:00Z`)

### Quality Control

- **Range checks:**
  - canopy_height: Flag if <0 m or >50 m
  - canopy_height: Flag if change >0.5 m between consecutive records (likely error)

### Temporal Application

Dynamic metadata applies from its timestamp until the next change:
- Record at `2014-11-05 12:30` with height `0.06` applies to all flux data from `2014-11-05 12:30` onwards
- Until next record at `2014-12-01 12:00` with height `0.05`
- EddyPro processing must use correct canopy height for each flux measurement period

---

## Storage

**S3 path:**
```
s3://flux-data/flux/ancillary/dynamic-metadata/
└── site=PLYNL/
    └── data.txt
```

---

## References

- EddyPro documentation: Dynamic metadata requirements