# 008. Apache Beam

Status: \[draft ~~\| proposed \| rejected \| accepted \| superseded by
x~~\]

Authors: Matt Brown

Deciders: Matt Brown, Dominic Ginger

Consulted: Faiza Samreen, Mike Brown

Date: 2024-11-08

## Context and Problem Statement

The rechunking of data as the first stage of the gridded data tools
product is computationally expensive. To complete in a reasonable amount
of time it needs to be parallelized, and there are many architecture
options for doing this.

## Decision Drivers

- Integrates well with existing libraries

- Is reliable for variable sizes and types of gridded data

- Independent of underlying compute platform (e.g. AWS, JASMIN LOTUS
  etc.)

## Considered Options

- Apache Beam

- Apache Airflow

- Argo

- Polars

- Dask

- Spark

## Decision Outcome

Chosen option: Apache Beam, because it is what is used by
pangeo-forge-recipes. Pangeo-forge-recipes is a wrapper around Beam,
creating functions specifically designed to do the task (rechunking and
conversion to zarr) that we want to do, without us having to construct
them from scratch in Beam ourselves. It can also be deployed via Dask,
Spark or Flink, among others, so does not tie us to a particular
platform or parallelization library. It is specifically designed to
handle the data sizes that we are likely to encounter. It is
well-supported by the pangeo community.

The main advantages of using Apache Beam over using Dask, Spark or Flink
directly are that we maintain the ability to use any of these via Beam's
various runners with minimal changes to the pipeline code (the script
that sets out the jobs we need to do to convert and rechunk the data),
and make the pipeline code easier for users to understand and write/edit
if necessary.

### Positive Consequences

- Much less development work needed (already been done by
  pangeo-forge-recipes)

- Not tied to one particular platform or parallelization engine

- Good support via pangeo forge community

### Negative Consequences

- Less control over the product (changes to pangeo-forge-recipes might
  affect the functionality the product)

- Dependent on pangeo-forge-recipes for updates and bugfixes etc., which
  affects development timelines and causes issues if it becomes
  unsupported

- Harder to debug than using Dask/Spark/Flink directly

## Pros and Cons of the Options

### \[Beam\]

See above

<https://beam.apache.org/>

###  \[Airflow\]

- Good, because it's easily deployed and available on AWS

- Bad, because it's expensive

- Bad, because it is a workflow/pipeline manager more than a compute
  library, so doesn't really help us handle the large compute load

- Bad, because we'd be tied to AWS unless we went through the effort of
  deploying it somewhere ourselves

<https://airflow.apache.org/>

### \[Argo\]

- Good, because it's easily deployed and available on AWS

- Good, because it's widely used and well documented

- Bad, because it is a workflow/pipeline manager more than a compute
  library, so doesn't really help us handle the large compute load

- Bad, because we'd be tied to AWS unless we went through the effort of
  deploying it somewhere ourselves

<https://argoproj.github.io/workflows/>

### \[Polars\]

- Good, because it's easily deployed and available as a python package

- Good, because it's essentially a faster version of pandas

- Bad, because it is only so far designed to handle tabular data, not
  gridded, which would mean major development effort to adapt it

<https://pola.rs/>

### \[Dask\]

- Good, it has a big user base and plenty of support (including within
  EDS/UKCEH)

- Good, because it's already built into xarray, the major gridded data
  handling python library

- Good, because it has great built-in diagnostics

- Good because JASMIN have a dask-gateway running on LOTUS (their HPC
  resource), one of our compute options

- Bad, because it's not as optimized as Beam is as it tries to be the
  "jack of all trades" for any type of parallelization and is thus very
  generalized instead

- Bad, because it requires more manual tweaking for each specific
  workflow (e.g. in terms of memory management), whereas Beam, in
  theory, can sit on top of dask and handle all that for us

<https://www.dask.org/>

### \[Spark\]

- Good, because most popular compute platform, used widely in industry.

- Good, lots of resources and support available

- Bad, because it's not integrated into xarray, which we'll very likely
  be using

- Bad, because it might not be easily possible to deploy it on JASMIN,
  one of our options for compute
