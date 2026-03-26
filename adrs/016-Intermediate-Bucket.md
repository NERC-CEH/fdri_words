# 016 Use of an intermediate bucket

- Status: Agreed by Mike Brown on 25th March, Dom Ginger was also consulted on the agreed solution

## Context and Problem Statement

In the Flux pipeline, EddyPro produces output files which need further processing before they are useful.  They also need to be retained to avoid expensive EddyPro re-runs if the required processing configuration changes.  Also, some of the outputs from EddyPro ("co-spectra") can be used as _inputs_ to future runs to improve precision/uncertainty.

The language in this ADR avoids the "level -1" etc naming scheme.

## Decision Drivers

- clarity about what data products are "final"

- ability to use data produced in previous runs


## Considered Options

- Option 1: separate "intermediate data" bucket (in addition to "raw", "ingested", "processed")

- Option 2: store all outputs of any kind in "processed" bucket

## Decision Outcome

Option 2: store all outputs of any kind in "processed" bucket

### Positive Consequences

- No Terraform changes required to create/manage new bucket

- No logic required in Timeseries Processor or other components to decide which bucket to place outputs

### Negative Consequences

- Some files in processed bucket will require further processing before they are usable

## Pros and Cons of the Options

### Separate "intermediate" bucket

Create an additional bucket and use it to place intermediate data products.

- Bad, because it's additional administrative overhead to manage an extra bucket in terms of permissions, lifecycle and developer experience

- Good, because it's obvious and clear what status outputs have

### Store all outputs in "processed"

Store everything that's the output of some processing in the "processed" bucket.

- Good, because it's simple

- Good, because it doesn't require any changes to infrastructure

- Bad, because it may not be clear that some data products are not fully processed and ready for publication/use
