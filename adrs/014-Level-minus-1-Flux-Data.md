# 014. S3 Bucket Architecture for Raw Flux Data

- Status: proposed

## Context and Problem Statement

The FDRI Eddy Covariance data processing system needs to store high-frequency (20 Hz) raw flux data (Level -1). Should this Level -1 raw data be stored in the same bucket as existing time series data, or in a separate bucket? How should we organize the raw data bucket for optimal query performance and cost management?

Note: Processed data will be stored in separate buckets.

## Decision Drivers

- Query performance through partition pruning
- Cost optimization via lifecycle policies
- Operational simplicity
- Scalability
- Reprocessing efficiency

## Considered Options

- Option 1: Single shared Level -1 bucket with time series data (`ukceh-fdri-staging-timeseries-level-m1/flux/...`)
- Option 2: Separate Level -1 bucket with day-level partitioning (`ukceh-fdri-staging-flux-level-m1/site/year/month/day/...`)
- Option 3: Separate Level -1 bucket with hour-level partitioning

## Decision Outcome

Chosen option: "Option 2: Separate Level -1 bucket with day-level partitioning", because flux data has significantly different volume and lifecycle characteristics than time series data, and hourly queries are not expected for this dataset. Day-level partitioning provides sufficient granularity for typical query patterns (site and date-based) while maintaining operational simplicity.

Level -1 bucket structure (raw data ingestion):
```
s3://ukceh-fdri-staging-flux-level-m1/
└── site={site}/year={year}/month={month}/day={day}/
    └── TOA5_{SITE}_FluxRaw_{YYYYMMDD}_{HHMM}.dat

Example: site=PLYNL/year=2024/month=08/day=14/TOA5_PLYNL_FluxRaw_20240814_0900.dat
```

### Positive Consequences

- Query costs reduced through partition pruning at day level
- Simpler partition structure reduces operational complexity
- Independent lifecycle policies with automatic tiering to lower-cost storage classes
- Clear operational boundaries for monitoring and access control

### Negative Consequences

- Additional bucket to monitor and manage
- Cross-bucket queries require IAM permissions for both buckets

## Pros and Cons of the other Options

### Option 1: Single shared Level -1 bucket with time series data

- Good, because unified Level -1 management and simpler integration
- Bad, because mixed access patterns (flux 20 Hz vs standard time series) and difficult to set independent lifecycle policies

### Option 3: Separate Level -1 bucket with hour-level partitioning

- Good, because maximum query optimization through finest-grained partitioning
- Good, because enables efficient hour-specific queries
- Bad, because adds unnecessary complexity given hourly queries are not expected
- Bad, because requires more partition management overhead

## Links

- [AWS S3 Best Practices for Data Lakes](https://docs.aws.amazon.com/prescriptive-guidance/latest/defining-bucket-names-data-lakes/welcome.html)
- [Hive Partitioning Guide](https://docs.aws.amazon.com/athena/latest/ug/partitions.html)
