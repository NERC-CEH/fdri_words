# Handling errors when dataset dependencies fail to process in the timeseries processor pipeline

The PE dataset has many data dependencies, with some independent 'branches'. 
Consider the case where one (or more) dependencies from one branch fail to process:

    PE 1D PROCESSED
    |
    └── PE 30Min PROCESSED
        |
        ├── G 30Min PROCESSED
        |   |
        |   ├── G1 30Min PROCESSED 
        |   |   └── G1 30Min RAW
        |   |
        |   └── G2 30Min PROCESSED
        |       └── G1 30Min RAW
        X
        └── SWIN, SWOUT, LWIN, LWOUT 30Min PROCESSED
            └── SWIN, SWOUT, LWIN, LWOUT 30Min RAW

In the case above, neither of the top two parent classes will be calculated correctly.

## What does it mean for processing to fail?
The pipeline could fail at any stage due to a bad dataset. This is separate from QC checks. Need to consider implementing error handling at all stages: LOAD, PROCESS, QC, INFILL, CORRECTION, DERIVATION, AGGREGATION, SAVE.

## Questions: 
1. Do we want to track data processing issues? 
2. Is there a use case for saving datasets that are independent of the bad dataset? We don't want to discard data that processes correctly, but when would that data be used? When performing a calculation, data is not retrieved from that which was previously processed and saved, but is always recalculated as it is just as quick to do so. Therefore it seems unnecessary to save data that processed correctly in a calculation that involved processing errors, unless we want to track data processing issues.

## Proposals for error handling:
- **Option A**: Pipeline is terminated. No data is saved. 
    - **Pros:** Easiest to implement, minimizes use of resources. 
    - **Cons:** discards processed data, no way to track if there has been processing issues in the past.
- **Option B**: Pipeline is terminated. All data that was processed without failing is saved. 
    - **Pros:** Easy to implement, minimal use of resources. 
    - **Cons:** Does not tell us if independent branches were passing or failing processing.
- **Option C**: Pipeline continues, but only datasets that are independent of the failing dataset are processed and saved. No processing of parent classes with dependencies failing processing. 
    - **Pros:** No processed data is discarded, all data that can be processed is processed.
    - **Cons:** Harder to implement, uses more resources, stores data that may not be used.
- **Option D**: Pipeline continues, but only datasets that are independent of the failing dataset are processed and saved. No processing of parent classes with dependencies failing processing. QC flags are added to any datasets that fail to be processed and to any parent datasets. 
    - **Pros:** No processed data is discarded, all data that can be processed is processed, additional information on problem datasets.
    - **Cons:** Harder to implement, uses more resources, stores data that may not be used.

## Testing
Need to add units tests to test error handling when processing fails.