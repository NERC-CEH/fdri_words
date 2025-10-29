# 011: Metadata-Driven DAG Architecture for Time Series Processing

Status: proposed
Authors: Richard Smith
Date: 2025-10-28

## Context and Problem Statement

The current time series data processing pipeline uses the metadata API to help define the workflows dynamically.
For a given site(s), resolution, and variable(s), it retrieves dataset metadata, identifies dependencies and 
processing configurations, and executes a fixed sequence of steps:

Gather metadata > Load data > Corrections > QC > Infill > Derive / aggregate variables

This approach works well for straightforward datasets with simple dependency chains, but it has two key limitations:

### 1. Shallow dependency traversal
- The current system only follows direct dependencies listed in the dataset metadata.
- Dependencies appearing deeper within configuration files are not recursively resolved.
- This can result in missing prerequisite data or incorrect execution order when dependent variables must first be 
  processed.

A concrete example of this is requesting the processing of **LWIN** (longwave inward radiation). One of the QC checks
for this is called ["nr01temp"](https://dri-metadata-api.staging.eds.ceh.ac.uk/id/data-processing-configuration/cosmos-bunny-lwin_30min_raw-nr01_temp), 
which has a dependency on the **TNR01C** variable. In the current processor, the dependency and configuration 
searching stops here. However, the **TNR01C** variable has its own QC and infilling configurations, with potential 
additional dependencies, that are not gathered.

### 2. Linear processing order
- The pipeline currently runs datasets through a fixed linear stage sequence - there is no mechanism to dynamically 
  reorder tasks based on actual dependency structure
- This model starts to breaks down when, for example, a derived or aggregated variable must be produced *before* it can 
  be used by another variable. An example of this is the daily rainfall, which requires 30 minute rainfall to be 
  aggregated from 1 minute rainfall. Workarounds can be put in place, but this increases the complexity. 

## Considered Options

This proposal outlines a **metadata-driven Directed Acyclic Graph (DAG)** method to orchestrate dataset processing.

> [!NOTE]
> I've used AI (ChatGPT, Claude) to help me structure this proposal, and help code a prototype system that provides
> example of it being used.

**Key Elements of the new approach:**

1. **Recursive Dependency Discovery**
   - Epimorphics have provided a recursive dependency endpoint: `/id/dataset/{id}/_all_dependencies.json`
     - This provides the 'direct' dataset dependencies for a given parent
     - For example, a parent of Net Radiation (RN) would provide the metadata for: SWIN_PROCESSED, SWIN_RAW, 
       SWOUT_PROCESSED, SWOUT_RAW, LWIN_PROCESSED, LWIN_RAW, LWOUT_PROCESSED, LWOUT_RAW
   - Gather dependencies from processing configurations (QC, infill, correction) **and recurse through these to get
     further dependencies**
   - Ensures all datasets required for any process are known

2. **DAG Builder**
   - Dependencies are held within a "DAG", allows us to know which datasets are dependents of which
   - Essentially a dictionary of `{parent dataset ID: [dependent1, dependent2, etc]}`
   - Dependents can exist in the list of multiple parent datasets

graph TD

  %% === Top-level Derived Variable ===
  RN_PROCESSED["RN_30MIN_PROCESSED"]

  %% === Processed Dependencies ===
  LWIN_PROC["LWIN_30MIN_PROCESSED"]
  LWOUT_PROC["LWOUT_30MIN_PROCESSED"]
  SWIN_PROC["SWIN_30MIN_PROCESSED"]
  SWOUT_PROC["SWOUT_30MIN_PROCESSED"]

  %% === Raw Dependencies ===
  LWIN_RAW["LWIN_30MIN_RAW"]
  LWOUT_RAW["LWOUT_30MIN_RAW"]
  SWIN_RAW["SWIN_30MIN_RAW"]
  SWOUT_RAW["SWOUT_30MIN_RAW"]

  %% === Shared Lower-Level Dependencies ===
  BATTV_RAW["BATTV_30MIN_RAW"]
  SCANS_RAW["SCANS_30MIN_RAW"]
  TA_RAW["TA_30MIN_RAW"]
  TNR01C_RAW["TNR01C_30MIN_RAW"]
  LWIN_UNC_RAW["LWIN_UNC_30MIN_RAW"]
  LWOUT_UNC_RAW["LWOUT_UNC_30MIN_RAW"]

  %% === Relationships ===
  RN_PROCESSED --> LWIN_PROC
  RN_PROCESSED --> LWOUT_PROC
  RN_PROCESSED --> SWIN_PROC
  RN_PROCESSED --> SWOUT_PROC

  LWIN_PROC --> LWIN_RAW
  LWOUT_PROC --> LWOUT_RAW
  SWIN_PROC --> SWIN_RAW
  SWOUT_PROC --> SWOUT_RAW

  %% --- LWIN RAW deps ---
  LWIN_RAW --> BATTV_RAW
  LWIN_RAW --> LWIN_UNC_RAW
  LWIN_RAW --> SCANS_RAW
  LWIN_RAW --> TA_RAW
  LWIN_RAW --> TNR01C_RAW

  %% --- LWOUT RAW deps ---
  LWOUT_RAW --> BATTV_RAW
  LWOUT_RAW --> LWOUT_UNC_RAW
  LWOUT_RAW --> SCANS_RAW
  LWOUT_RAW --> TA_RAW
  LWOUT_RAW --> TNR01C_RAW

  %% --- SWIN RAW deps ---
  SWIN_RAW --> BATTV_RAW
  SWIN_RAW --> SCANS_RAW

  %% --- SWOUT RAW deps ---
  SWOUT_RAW --> BATTV_RAW
  SWOUT_RAW --> SCANS_RAW

  %% === Styling ===
  classDef processed fill:#dbeafe,stroke:#1e3a8a,stroke-width:2px,color:#000;
  classDef raw fill:#fef3c7,stroke:#92400e,stroke-width:2px,color:#000;
  classDef base fill:#dcfce7,stroke:#166534,stroke-width:2px,color:#000;

  class RN_PROCESSED processed
  class LWIN_PROC,LWOUT_PROC,SWIN_PROC,SWOUT_PROC processed
  class LWIN_RAW,LWOUT_RAW,SWIN_RAW,SWOUT_RAW raw
  class BATTV_RAW,SCANS_RAW,TA_RAW,TNR01C_RAW,LWIN_UNC_RAW,LWOUT_UNC_RAW base
