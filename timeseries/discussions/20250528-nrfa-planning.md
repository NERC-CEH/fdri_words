### 2025.05.28 NRFA Planning

We discussed some aspects related to how we integrate the NRFA workflow into the time series product. 

Some agreed high-priority actions to get the ball rolling include:
- Rationalise the measuring-authority ingestors (EA and SEPA from APIs, NRW todo)
  - Consider having an NRFA-ID lookup within the ingestor, and saving data to a bucket with format: 
> `ukceh-fdri-staging-timeseries-level-0\nrfa\dataset=<e.g. daily_flow>\site=<nrfa_id>\<maybe date partition>\data.parquet`
  - Progress work on NRW ingestor (file-based, some progress made but no data being saved out to a bucket)
- Get a pilot end-to-end pipeline working for NRFA daily flow data
  - Includes getting some NRFA stations into the metadata service, with appropriate configs to drive the pipeline
  - Try and use the current pipeline architecture as much as possible to see if it "just works".  May need tweaks as we go.
- Get some data in the UI
  - Set up an "NRFA" page, similar to FDRI or COSMOS
  - Just get some of the raw EA/SEPA data in there for now as proof of concept
    - Needs associated API changes
  - When daily flow pipeline is done, get some of that data in the UI
- Basics of a manual QC UI
  - Proof of concept - marking points from charts and/or tables, being able to flag them and add a comment
- Flag management - follow up with NRFA team to understand what they do with the measuring authority flags
