# DP2 FDRI time series data management and processing system — Task Prioritisation

**Draft — April 2026**

---

## Milestones

**September 2026 (Soft Launch):** 
  - FDRI station data received, QC'd and displayed from current sites.
  - COSMOS-UK data received, QC'd / processed and displayed to demonstrate integration of data from different networks.
  - NRFA data simply downloaded from APIs and displayed in UI
  - EA / SEPA / NRW 15 minute rainfall ingested from APIs and displayed in UI for sites in and around FDRI catchments
  - Additional published 3rd party datasets incorporated - no QC / processing required, but displayed in UI - Plynlimon weather station and flow data 
  - Datasets linked through to catalogue records and spatial viewer / infrastructure.
    
**March 2027 (End of Year — Y3 Objective):** 
  - All WP1 station types able to send data into FDRI systems
  - FDRI stations able to be managed via AWS systems
  - Initial network monitoring interface available for WP1
  - Operational (beta) pipelines for FDRI station types, including manual QC
  - Operational (beta) pipeline for COSMOS-UK data, ready for switch over to use of FDRI systems as primary systems for COSMOS
  - Operational (beta) pipeline, including QC, for other 3rd party datasets - EA/SEPA/NRW 15 minute rainfall and river flows
  - Additional published 3rd party datasets incorporated
  - Beta version (not yet operational) of NRFA pipeline implemented including automated flagging, manual QC / comments and external sharing of comments
  - Beta version (not yet operational) of flux data processing from FDRI sites, with processed data received into time series systems
  - First version of automated ML QC approaches implemented 
  - Plan developed for how to incorporate uncertainty information (within data storage / metadata, and exported data formats)
 
### Priority Key

| Label | Meaning |
|-------|---------|
| 🟢 **Sept** | Target for September 2026 soft launch prototype |
| 🔵 **Mar 27** | Target for March 2027 operational beta |
| 🟡 **Later** | Future / nice-to-have / dependent on other work |

---

## 1. Infrastructure & Architecture

*Foundation work that everything else depends on.*

### S3 storage
(placeholder table)
| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| S3 repartitioning | 🟢 Sept | FPM-682 | To be undertaken when new AWS instance complete. See link https://github.com/NERC-CEH/fdri_discussions/discussions/2#discussioncomment-16086101 |

## 2. FDRI pipeline

### 


