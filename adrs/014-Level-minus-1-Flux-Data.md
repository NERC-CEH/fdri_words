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
- Option 2: Separate Level -1 bucket with basic day partitioning (`ukceh-fdri-staging-flux-level-m1/site/year/month/day/...`)
- Option 3: Separate Level -1 bucket with hour-level Hive partitioning

## Decision Outcome

Chosen option: "Option 3: Separate Level -1 bucket with optimized Hive partitioning", because flux data has significantly different volume and lifecycle characteristics than time series data. Hour-level Hive partitioning enables efficient data filtering and partition pruning, significantly reducing the amount of data scanned during queries and improving performance.

Level -1 bucket structure (raw data ingestion):
```
s3://ukceh-fdri-staging-flux-level-m1/
└── site={site}/year={year}/month={month}/day={day}/hour={hour}/
    └── TOA5_{SITE}_FluxRaw_{YYYYMMDD}_{HHMM}.dat

Example: site=PLYNL/year=2024/month=08/day=14/hour=09/TOA5_PLYNL_FluxRaw_20240814_0900.dat
```

### Positive Consequences

- Query costs substantially reduced through partition pruning
- Query performance significantly improved
- Independent lifecycle policies with automatic tiering to lower-cost storage classes
- Clear operational boundaries for monitoring and access control

### Negative Consequences

- Additional bucket to monitor and manage
- Cross-bucket queries require IAM permissions for both buckets

## Pros and Cons of the other Options

### Option 1: Single shared Level -1 bucket with time series data

- Good, because unified Level -1 management and simpler integration
- Bad, because mixed access patterns (flux 20 Hz vs standard time series) and difficult to set independent lifecycle policies

### Option 2: Separate Level -1 bucket with basic day partitioning

- Good, because clear separation of flux from time series and independent lifecycle policies
- Bad, because hour-specific queries must scan full day's data (no partition pruning benefit)

## Links

- [AWS S3 Best Practices for Data Lakes](https://docs.aws.amazon.com/prescriptive-guidance/latest/defining-bucket-names-data-lakes/welcome.html)
- [Hive Partitioning Guide](https://docs.aws.amazon.com/athena/latest/ug/partitions.html)
