# Timeseries

Documentation and notes about the timeseries project

## Contents

- [dri ui intro slides](dri-ui-intro-slides.html)
- [ways of working](ways-of-working.html)

## Repositories

### Applications 

- [dri-data-api](https://github.com/NERC-CEH/dri-data-api) - FastAPI application which provides a query frontend to timeseries data held in parquet files in s3 storage
- [dri-utils](https://github.com/NERC-CEH/dri-utils/) - Generic common code used mainly by the API project
- [dri-database-models](https://github.com/NERC-CEH/dri-database-models) - Postgres database schema definitions and migrations, mainly for use with the Phenocam extensions to the data API
- [dri-ingestion](https://github.com/NERC-CEH/dri-ingestion/) - Pipelines that load data from different sources into s3
- [dri-timeseries-processor](https://github.com/nerc-ceh/dri-timeseries-processor) - processing rules for derived timeseries from raw sensor data
- [time-stream](https://github.com/NERC-CEH/time-stream) - a standalone library for timeseries analysis

### Metadata

- [dri-metadata-api](https://github.com/NERC-CEH/dri-metadata-api/) - metadata API container build setup
- [fdri-discovery](https://github.com/NERC-CEH/fdri-discovery/) - support material and discussions

### Infrastructure

- [dri-infrastructure](https://github.com/NERC-CEH/dri-infrastructure/) - Terraform configuration for AWS
- [dri-infrastructure-k8s-staging](https://github.com/NERC-CEH/dri-infrastructure-k8s-staging/) - configuration for Kubernetes in AWS (EKS)


### Diagrams
- [diagrams/overview.drawio.png](diagrams/overview.drawio.png)
- [diagrams/tech-choices.drawio.png](diagrams/tech-choices.drawio.png)

### Discussions
- [discussions/20250528-api-planning](discussions/20250528-api-planning.html)
- [discussions/20250528-architecture-golf](discussions/20250528-architecture-golf.html)
- [discussions/20250528-nrfa-planning](discussions/20250528-nrfa-planning.html)
- [discussions/20250529-data-storage](discussions/20250529-data-storage.html)
