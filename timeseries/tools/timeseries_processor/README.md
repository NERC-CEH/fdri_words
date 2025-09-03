# Timeseries Processor
The timeseries processor application is part of the FDRI architecture and handles all the processing between **level 0** and **processed**.

<img src="./images/fdri_architecture.png" alt="FDRI architecture" height="400px">

This documentation will provide a higher level overview of the application. For guidance on how to run the application, and how to contribute, see the repository [README](https://github.com/NERC-CEH/dri-timeseries-processor).

## Table of contents
1. [Introduction](#introduction)
2. [Components](#components)
    1. [Inputs](#inputs)
    2. [Building timeseries IDs to process](#building-timeseries-ids-to-process)
    3. [Flags](#flags)
    4. [Corrections](#corrections)
    5. [Quality control](#quality-control)
    6. [Infilling](#infilling)
    7. [Aggregation and Derivation](#aggregation-and-derivation)
    8. [Outputs](#outputs)
3. [Glossary](#glossray)


## Introduction
The timeseries processor handles the processing and checking of timeseries data within the FDRI project and is powered by configurations available through the [metadata store](https://dri-metadata-api.staging.eds.ceh.ac.uk/doc/reference). It takes level 0 data, which has been ingested through the [ingester application](https://github.com/NERC-CEH/dri-ingestion), processes the data based on the configurations, and exports the data into a database.

The tool is a python application which takes a set of arguments (see [Inputs](#inputs)). The processor runs automatically at X every day via a workflow orchestration tool called Argo Workflows which is hosted in the FDRI kubernetes cluster. This is managed in the [kubernetes infrastructure repository](https://github.com/NERC-CEH/dri-infrastructure-k8s-staging). The application can also be run as a one-off job as and when required.

<[back to table of contents](#table-of-contents)>

## Components
The application can be split into several components, each of which will be discussed briefly below.

Insert flowchart

<[back to table of contents](#table-of-contents)>

### Inputs

---

The application takes a variety of user inputs entered as command-line arguments. These arguments define the date range and the timeseries IDs to be processed. A user can request the `ts_ids` directly, or use a combination of `sites`, `columns` and `periodicity`. A combination of these is not allowed and the processor will fail.

> --network (**required**):\
The network to process
- Must be a valid network (e.g cosmos or fdri)

> --period (**required**):\
The period of time to process
- Must be a valid [ISO8601 duration](https://docs.digi.com/resources/documentation/digidocs/90001488-13/reference/r_iso_8601_duration_format.htm)
- Must not have a time component
- Can be a combination of days, weeks, months and years

> --end_date (**optional**)\
The start date for processing
- Must be of the format YYYY-MM-DD
- If not provided then todays date is used

> --ts_id (**optional**): \
One or more specific ts_ids to process
- Each timeseries must be provided as a combination of the `site`, `column` and `periodicity` (as ISO8601) (e.g. alic1 pe PT30M)
- It is assumed that the ts_id corresponds to processed data, and that the network is the same as the one provided by --network argument

> --sites (**optional**)\
The site(s) to process
- If empty then all sites will be built
- Entered sites are checked against available sites in the metadata store and removed if not found
- sites must be seperated by a comma, be 5 characters long and not contain special characters
- sites can be lower or upper case

> --columns (**optional**)\
The column(s) to process
- If empty then all columns will be built
- Columns must be seperated by a comma (no spaces)
- Columns can be upper or lower case

> --periodicity (**optional**)\
The period(s) to process
- Must be a valid [ISO8601 duration](https://docs.digi.com/resources/documentation/digidocs/90001488-13/reference/r_iso_8601_duration_format.htm)
- Multiple periodicities must be seperated by a comma
- Can be upper or lower case

Some examples:

Get the last two days data for cosmos for all sites, columns and periodicities

```
python -m dritimeseriesprocessor --period=P2D --network=cosmos
```

Get the last two days data from 2024-03-05 for cosmos for all sites, columns and periodicities

```
python -m dritimeseriesprocessor --period=P2D --network=cosmos --end_date=2024-03-05
```

Get the last months data from 2024-03-05 for cosmos ALCI and BUNNY sites and all columns and periodicities

```
python -m dritimeseriesprocessor --period=P1M --network=cosmos --end_date=2024-03-05 --sites=alic1,bunny
```

Get the last two days data from 2024-03-05 for cosmos ALCI and BUNNY sites, variables TA and PA and all periodicities

```
python -m dritimeseriesprocessor --period=P2D --network=cosmos --end_date=2024-03-05 --sites=alic1,bunny --columns=TA,PA
```

Get the last two days data from 2024-03-05 for cosmos ALCI and BUNNY sites, variables TA and PA and a periodicity of 30 mins

```
python -m dritimeseriesprocessor --period=P2D --network=cosmos --end_date=2024-03-05 --sites=alic1,bunny --columns=TA,PA --periodicity=PT30M
```

Get the last two days data from 2024-03-05 for certain ts_ids

```
python -m dritimeseriesprocessor --period=P2D --network=cosmos --end_date=2024-03-05 -ts-id alic1 pe PT30M --ts-id bunny ta P1D`
```

<[back to table of contents](#table-of-contents)>

### Building Timeseries IDs to process

---

The processor uses the arguments above to build a set of timeseries IDs to process, and collects any metadata that is required to complete the processing.

The first stage is to collect the timeseries IDs based on the arguments. These are generated by sending the arguments to the timeseries view for the [datasets](https://dri-metadata-api.staging.eds.ceh.ac.uk/id/dataset?_limit=10) endpoint in the metadata store. This gives a dictionary of timeseries IDs along with some metadata including the methodology. A `load` parameter is calculated indicated whether the data needs to be loaded (i.e. `raw` timeseries required for `processed` timeseries).

Each timeseries ID might have some other timeseries IDs that it is dependent on to be processed. There are two types of dependency:

**Processing dependencies**:
Each timeseries ID might have certain processing dependencies. These are generated by calling the [timeseries](https://dri-metadata-api.staging.eds.ceh.ac.uk/id/dataset?originatingSite=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fsite%2Fcosmos-bunny&originatingSite=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fsite%2Fcosmos-alic1&%40id=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fdataset%2Fcosmos-alic1precip_diag_30min_raw&%40id=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fdataset%2Fcosmos-alic1-battv_30min_raw&%40id=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fdataset%2Fcosmos-bunnyprecip_diag_30min_raw&%40id=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fdataset%2Fcosmos-bunny-scans_30min_raw&%40id=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fdataset%2Fcosmos-bunny-battv_30min_raw&%40id=http%3A%2F%2Ffdri.ceh.ac.uk%2Fid%2Fdataset%2Fcosmos-alic1-scans_30min_raw&_view=timeseries&_limit=50) view for the dataset endpoint.

**Derivation dependencies**:
Each timeseries ID might be dependant on other timeseries IDs (for example, a `processed` timeseries will require the associated `raw` timeseries). These are generated by calling the [dependencies](https://dri-metadata-api.staging.eds.ceh.ac.uk/id/dataset/cosmos-alic1-swout_30min_processed/_dependencies) view for the dataset endpoint in the metadata store.

Below is an example output of these processes when the processing is run with the following arguments.

```
python -m dritimeseriesprocessor --period=P2D --network=cosmos --sites=eastb --columns=WD --periodicity=PT30M
```

```
{
    # Timeseries ID built from the arguments
    "http://fdri.ceh.ac.uk/id/dataset/cosmos-eastb-wd_30min_processed":
    {
        "ts_def": "http://fdri.ceh.ac.uk/ref/cosmos/time-series/wd_30min_processed",
        "resolution": "PT30M",
        "periodicity": "PT30M",
        "processing_level": "processed",
        "sourceBucket": "ukceh-fdri-staging-timeseries-processed",
        "sourceDataset": "PROCESSED_DATA_30MIN",
        "sourceColumnName": "WD",
        "sourceSite": "EASTB",
        "method_type": "process",
        "inputs":
        [
            "http://fdri.ceh.ac.uk/ref/cosmos/time-series/wd_30min_raw"
        ],
        "load": False
    },
    # Dependent timeseries ID
    "http://fdri.ceh.ac.uk/id/dataset/cosmos-eastb-scans_30min_raw":
    {
        "ts_def": "http://fdri.ceh.ac.uk/ref/cosmos/time-series/scans_30min_raw",
        "resolution": "PT30M",
        "periodicity": "PT30M",
        "processing_level": "raw",
        "sourceBucket": "ukceh-fdri-staging-timeseries-level-0",
        "sourceDataset": "LIVE_SOILMET_30MIN",
        "sourceColumnName": "SCANS",
        "sourceSite": "EASTB",
        "inputs":
        [],
        "load": True
    },
    # Dependent timeseries ID
    "http://fdri.ceh.ac.uk/id/dataset/cosmos-eastb-battv_30min_raw":
    {
        "ts_def": "http://fdri.ceh.ac.uk/ref/cosmos/time-series/battv_30min_raw",
        "resolution": "PT30M",
        "periodicity": "PT30M",
        "processing_level": "raw",
        "sourceBucket": "ukceh-fdri-staging-timeseries-level-0",
        "sourceDataset": "LIVE_SOILMET_30MIN",
        "sourceColumnName": "BATTV",
        "sourceSite": "EASTB",
        "inputs":
        [],
        "load": True
    },
    # Dependent timeseries ID
    "http://fdri.ceh.ac.uk/id/dataset/cosmos-eastb-wd_30min_raw":
    {
        "ts_def": "http://fdri.ceh.ac.uk/ref/cosmos/time-series/wd_30min_raw",
        "resolution": "PT30M",
        "periodicity": "PT30M",
        "processing_level": "raw",
        "sourceBucket": "ukceh-fdri-staging-timeseries-level-0",
        "sourceDataset": "LIVE_SOILMET_30MIN",
        "sourceColumnName": "WD",
        "sourceSite": "EASTB",
        "inputs":
        [],
        "load": False
    }
}
```

All the metadata required to process the requested timeseries IDs has now been collected. Data for each timeseries ID is loaded into a [Timestream](https://nerc-ceh.github.io/time-stream/) object before being passed into the processing stages.

<[back to table of contents](#table-of-contents)>

### Flags ###

---

A flagging system is used to keep track of what tests have been undertaken as part of the processing. Each column will have a set of core tests that are checked and then additional flags are added to the timestream object based on what component of the processing they relate to. For example, the timeseries for `SWOUT` has core tests and ones for all the components.

```
┌─────────────────────────┬───────┬─────────────────┬───────────────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_PR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---           ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64           ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═══════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ 1.265 ┆ 0               ┆ 0             ┆ 0             ┆ 0                 │
```

Configurations for the tests that can be run on the timeseries are currently stored within the repository, but these will likely be moved to the metadata store. Each test contains an `id` which is a multiple of two (representing a "bit" in a binary number) and is used as part of a bitwise flagging system.

```
        "corrected": {
            "name": "Corrected",
            "description": "Data point has been adjusted from original value.",
            "symbol": "C",
            "id": 1
        },
        "estimated": {
            "name": "Estimated",
            "description": "Data point is an estimate in some way, either through infilling techniques or incomplete derivation.",
            "symbol": "E",
            "id": 2
        },
        "missing": {
            "name": "Missing",
            "description": "Data point was not recorded.",
            "symbol": "M",
            "id": 4
        },
        "removed": {
            "name": "Removed",
            "description": "Data point was removed by QC.",
            "symbol": "R",
            "id": 8
        },
        "suspicious": {
            "name": "Suspicious",
            "description": "Data point is potentially erroneous or requiring further investigation.",
            "symbol": "S",
            "id": 16
        },
        "unchecked": {
            "name": "Unchecked",
            "description": "Data point has not been verified by QC.",
            "symbol": "U",
            "id": 32
        }
```

If the data point fails a test, then the `id` is added to the flag column. This results in a integer which is a unique identifier for which tests have failed.

```
┌─────────────────────────┬───────┬─────────────────┬───────────────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_PR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---           ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64           ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═══════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ 1.265 ┆ 50               ┆ 7             ┆ 10             ┆ 0                 │
```
For example, SWOUT failed the `estimated`, `suspicious` and `unchecked` core tests, and didnt fail any infilling tests.


### Corrections

---

Corrections are where known adustments are purposely made to data. If for example, a sensor has had an incorrect calibration value applied, the raw data can be corrected at this point.

There are three basic adjustment methods:
1. **Addition**: Add a correction factor to values. y=x + C
2. **Scalar**: Multiply values by a correction factor. y=Cx
3. **Power**: Raise values to the power of a correction factor. y=x^C

Additional methods can also be added for more bespoke corrections, for example the long wave correction method where correcting long wave value affected by incorrect calibration values is more complex than a simple scalar.

Correction methods are registered in the codebase:
```
src/metadata_manager/models/methods/correction_methods.json
```
```
{
    "add": {
        "name": "ADD",
        "description": "Sum the data point and correction value. E.g. y=x+ C, where x is the data point and C is the change factor.",
        "id": 1,
        "function_name": "add" 
    },
    "lw_corr": {
        "name": "LW_CORR",
        "description": "Correction for long wave radiation where calibration values are incorrect.",
        "id": 2,
        "function_name": "lw"
    },
    "scalar": {
        "name": "SCALAR",
        "description": "Multiply the data point by a correction factor. E.g. y=Cx where x is the data point and C is the correction factor.",
        "id": 4,
        "function_name": "multiply"
    },
}
```
Each correction method includes an `id` that is used as a [flag](#flags) value where the method is applied.

The methods themselves are saved as classes here:
```
src/dritimeseriesprocessor/correcting/operations.py
```
Each has an `apply` method where the correction method is implemented, and a `name` attribute that matches the "function_name" in the method registery.

The data on which each method is applied is determined by metadata configs. Each config references:
- **A timeseries**, e.g. 30 minute air pressure at site Bunny Park
- **A correction method** (and parameters), e.g. apply scalar method with correction factor 1.23
- **A date period**, e.g. apply correction between 1-1-2020 10:00 and 2-2-2020 17:30

Each correction method requires a set of parameters. For the addition, scalar and power methods, this is a single numeric correction factor. For other methods this could be more.
There are three types of parameter a correction method can take:
- **Correction factors** - These are always numeric
- **Dependant timeseries** - Other datasets required to make the adjustment, for example, there is a wind direction correction the requires UX and UY wind components
- **Site attributes** - Site information required to make the adjustment, for example, an air pressure correction that requires site altitude.

With all this information the correction code is able to apply the adjustments and flag the data accordingly.

<[back to table of contents](#table-of-contents)>

### Quality Control

---

Quality control (QC) is the process of identifying and handling data points that appear may be erroneous. The timeseries processor applies a series of QC tests to each timeseries, flagging data points according to the outcome of these tests.

There are three base types of QC tests:
1. **Range test**: Ensure values fall within expected minimum and maximum thresholds.
2. **Spike test**: Pick out spikes above a given threshold.
3. **Comparison test**: Compare values against a threshold, either above, bleow or equal to.

These come as methods of the TimeSeries object from TimeStream. The comparison test is used in particular as the base to many bespoke tests.
QC methods are registered in the codebase:
```
src/metadata_manager/models/methods/qc_methods.json
```
Example configuration:
```
{
    "range": {
        "name": "Range check",
        "description": "Checks if the value falls within a specified range",
        "id": 1,
        "function_name": "range",
        "arg_mapping": {
            "min_value": "lt",
            "max_value": "gt"
        },
        "kwargs": {
            "within": false
        }
    },
    "battery_v": {
        "name": "Battery voltage check",
        "description": "Checks that the battery voltage level is above the threshold",
        "id": 2,
        "function_name": "comparison",
        "arg_mapping": {
            "compare_to": "lt"
        },
        "kwargs": {
            "operator": "<"
        }
    },
    "samples": {
        "name": "Samples check",
        "description": "Checks if the number of samples taken in measuring period are too low.",
        "id": 4,
        "function_name": "comparison",
        "arg_mapping": {
            "compare_to": "lt"
        },
        "kwargs": {
            "operator": "<"
        }
    },
    "error_code": {
        "name": "Error codes check",
        "description": "Check for specific error codes",
        "id": 8,
        "function_name": "comparison",
        "arg_mapping": {
            "compare_to": "value"
        },
        "kwargs": {
            "operator": "is_in"
        }
    },
    "spike": {
        "name": "Spike check",
        "description": "Checks for individual spikes in data that exceed a threshold",
        "id": 16,
        "function_name": "spike",
        "arg_mapping": {
            "threshold": "gt"
        }
    },
}
```
Each QC test includes an `id` used for flagging.

The data on which each test is applied is determined by metadata configs. Each config references:
- **A timeseries**, e.g. 30 minute air pressure at site Bunny Park
- **A QC test** (and parameters), e.g. spike checks with threshold 100

Each test requires a set of parameters. There are a number of parameter a QC test can have:
- **Dependant timeseries** - Other datasets required to test against, for example, look at battery voltage being high enough to trust a pressure sensor reading.
- **Threshold values** - For example, min/max for range checks. This can also include times, for example, flag any values between 00:30 and 01:00.

When a data point fails a QC test, the corresponding flag is set using the bitwise system described in the [Flags](#flags) section. This allows multiple QC outcomes to be tracked for each data point.

QC results are stored in dedicated flag columns (e.g., `SWOUT_QC_FLAG`)


<[back to table of contents](#table-of-contents)>

### Infilling

---

Sample text here

<[back to table of contents](#table-of-contents)>

### Aggregation and Derivation

---

Sample text here

<[back to table of contents](#table-of-contents)>

### Outputs

---

Processed data is written to the [processed](https://eu-west-2.console.aws.amazon.com/s3/buckets/ukceh-fdri-staging-timeseries-processed?region=eu-west-2&tab=objects&bucketType=general) s3 bucket and is partitioned by network, date, site and resolution.

If data already exists in the partition, then only the rows and columns that have changed are updated.

<[back to table of contents](#table-of-contents)>



## Glossary

**Level minus 1**: Level minus 1 data is the raw data directly from the sensor.

**Level 0**: Level 0 data is the raw data (level minus 1) from the sensor that has been validated against an expected schema and saved to parquet files.

**Timeseries definition**: A timeseries defined by a network, column, processing level and period e.g. `http://fdri.ceh.ac.uk/ref/cosmos/time-series/precip_30min_raw`

**Timeseries ID**: A timeseries definition for a particular site e.g. `cosmos-chobh-precip_30min_raw`. A timeseries definition will contain several timeseries IDs.

<[back to table of contents](#table-of-contents)>
