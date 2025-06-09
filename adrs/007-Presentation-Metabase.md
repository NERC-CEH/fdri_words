# 007. Presentation - Metabase

Status: proposed

Authors: Dom Ginger

Deciders: \[List of everybody involved in the decision\]

Consulted: \[Who needs to be consulted\]

Date: 2024-09-24

## Context and Problem Statement

We have data flowing through our data pipeline and now need to present
it back to users. We know we have at least 2 types of users, field
engineers and data scientists who use tsp. We have a few options on how
to present this data, this ADR focuses on Metabase
<https://www.metabase.com/> as a potential alternative to building a
solution from scratch.

Metabase has the potential to solve 2 problems, first to quickly get
something in front of users to start guiding discussions and secondly be
suitable enough for a long time solution.

## Decision Drivers

- Quick to get started with

- Operational complexity

- Cloud agnostic

- Ease of use

- Looks good

- Flexibility

## Considered Options

- Metabase

- Apache Superset

- Custom front end

- Grafana

- redash

## Decision Outcome

Chosen option: metabase, comes out best.

<https://www.metabase.com/>

![](/media/image.png){width="6.5in" height="4.59375in"}Metabase
dashboard using cosmos data from parquet files on s3

### Positive Consequences

- Quick to get started with

- User friendly interface (either dashboard only, or sql only for
  advanced users)

### Negative Consequences

- lose control over performance/caching (maybe a proxy could fix this)

- Missing features could mean more tools needed

- requires a postgres/mysql db to store internal config

- keeps crashing with 6GB H2 database locally

- some features are paywalled (e.g
  <https://www.metabase.com/docs/latest/installation-and-operation/serialization>
  )

- Limited to SQL queries, all data needs to be accessed via SQL

## Pros and Cons of the Options

### Apache Superset

<https://superset.apache.org/>

- Good, more flexible than metabase (supports python for custom
  features)

- Good, no paywalled features

- Bad, steeper learning curve

- Bad, more complex deployment

- Bad, cannot get it running locally

###  Custom front end

Written from scratch (would probably be <https://react.dev/> and
<https://d3js.org/> based)

- Good, completely customisable

- Good, can be a one stop shop (even iframe for the loggernet cloud)

- Bad, lots of work
