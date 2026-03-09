# Timeseries

Documentation and notes about the timeseries project

## Contents

- [dri ui intro slides](dri-ui-intro-slides.html)
- [ways of working](ways-of-working.html)

## Repositories

- [dri-data-api](https://github.com/NERC-CEH/dri-data-api) - FastAPI application which provides a query frontend to timeseries data held in parquet files in s3 storage
- [dri-utils](https://github.com/NERC-CEH/dri-utils/) - Generic common code used mainly by the API project
- [dri-database-models](https://github.com/NERC-CEH/dri-database-models) - Postgres database schema definitions and migrations, mainly for use with the Phenocam extensions to the data API
- [dri-ingestion](https://github.com/NERC-CEH/dri-ingestion/) - Pipelines that load data from different sources into s3


### Diagrams
- [diagrams/overview.drawio.png](diagrams/overview.drawio.png)
- [diagrams/tech-choices.drawio.png](diagrams/tech-choices.drawio.png)

### Discussions
- [discussions/20250528-api-planning](discussions/20250528-api-planning.html)
- [discussions/20250528-architecture-golf](discussions/20250528-architecture-golf.html)
- [discussions/20250528-nrfa-planning](discussions/20250528-nrfa-planning.html)
- [discussions/20250529-data-storage](discussions/20250529-data-storage.html)
