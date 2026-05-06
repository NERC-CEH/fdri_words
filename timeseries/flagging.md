# Flags #


A flagging system is used to keep track of the data as it moves through the [processing](https://github.com/NERC-CEH/dri-timeseries-processor/blob/main/docs/index.md) pipeline.

There are two categories of flags:
1. [Core flags](#core-flags) - High level flags that give us general information on the data.
2. [Processing flags](#processing-flags) - These give us more detail on the processing that has occurred on the data.

Each timeseries dataset that runs through the processor has all the flag types added to the [TimeFrame](https://nerc-ceh.github.io/time-stream/api/time_frame.html) object it is held in. In all cases, a flag value of 0 means no flag.

For example, the TimeFrame object for `SWOUT` would look like this:
```
┌─────────────────────────┬───────┬─────────────────┬───────────--────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_CORR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---             ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64             ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═════════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ 1.265 ┆ 0               ┆ 0               ┆ 0             ┆ 0                 │
```
Don't worry about the meaning of each flag column yet, just note that we have columns:
- **time**: For the timestamps of the data
- **SWOUT**: The actual data
- **SWOUT_<flag_type>_FLAG**: Four flag columns

This is how all timeseries datasets start.

## Core flags ##

Core flags are used to provide high level information on data. Their meanings do not necessarily share
a common theme. They are designed to provide a simple insight into the data, that could be useful for a user
to know.

Here are the current core flags and their meanings:
```
{
    "corrected": {
        "name": "Corrected",
        "description": "Data point has been adjusted from original value.",
        "id": 1
    },
    "estimated": {
        "name": "Estimated",
        "description": "Data point is an estimate in some way, either through infilling techniques or incomplete derivation.",
        "id": 2
    },
    "missing": {
        "name": "Missing",
        "description": "Data point was not recorded.",
        "id": 4
    },
    "removed": {
        "name": "Removed",
        "description": "Data point was removed by QC.",
        "id": 8
    },
    "suspicious": {
        "name": "Suspicious",
        "description": "Data point is potentially erroneous or requiring further investigation.",
        "id": 16
    },
    "unchecked": {
        "name": "Unchecked",
        "description": "Data point has not been verified by QC.",
        "id": 32
    },
    "unsuccessful_correction": {
        "name": "UnsuccessfulCorrection",
        "description": "A correction was attempted but was unsuccessful due to missing input data.",
        "id": 64
    }
}
```
> **Note**: These flags are common across different networks, i.e. COSMOS, and FDRI will both use these same flags.

## Processing flags ##

As timeseries datasets are passed through the processing, they undertake three key processing steps:
1. Corrections
2. Quality control
3. Infilling

If any of these steps get applied to data, the flag system is used to record exactly what was done.
Firstly, the [core flags](#core-flags) play a part for each step...
- If data gets corrected, it will recieve a `corrected` core flag
- If data fails QC, it will recieve a `removed` core flag
- If data gets infilled, it will recieve an `estimated` core flag

These are designed to give a high level insight into the data.

The **processing flags** are there to provide the detail of each processing step. In other words they tell us exactly what was done to the data to either correct, QC, or infill it.

Hence, we have three sets of processing flags...

### Correction flags ###
Here are the flags for corrections within the COSMOS network:
```
{
    "Add": {
        "description": "Sum the data point and correction value. E.g. y=x+C, where x is the data point and C is the change factor.",
        "id": 1,
    },
    "LWCorrection": {
        "description": "Correction for long wave radiation where calibration values are incorrect.",
        "id": 2,
    },
    "Scalar": {
        "description": "Multiply the data point by a correction factor. E.g. y=Cx where x is the data point and C is the correction factor.",
        "id": 4,
    },
    "PACorrection": {
        "description": "Correct air pressure with bias calculated from mean sea level pressure.",
        "id": 8,
    },
    "Power": {
        "description": "Raise data point to power of correction factor. E.g. y=x^C where x is the data point and C is the correction factor.",
        "id": 16,
    },
    "WDCorrection": {
        "description": "Correct wind direction where wind sensor installed backwards.",
        "id": 32,
    },
    "Clip": {
        "description": "Clip values above or below threshold to the threshold.",
        "id": 64,
    }
}
```

### Quality control flags ###
Here are the flags for QC within the COSMOS network:
```
{
    "Range": {
        "description": "Data fell outside of legitimate min and max.",
        "id": 1,
    },
    "BatteryVoltage": {
        "description": "The battery voltage was too low to power the sensor properly.",
        "id": 2,
    },
    "Samples": {
        "description": "Too few samples were taken by the logger from the sensor within the measuring period.",
        "id": 4,
    },
    "ErrorCode": {
        "description": "The data value is an error code.",
        "id": 8,
    },
    "Spike": {
        "description": "Spike in the data detected.",
        "id": 16,
    },
    "Nr01Temp": {
        "description": "The NR01 sensor temperature was out of operating range, meaning data cannot be trusted.",
        "id": 32,
    },
    "HeatFluxPlateRemoval": {
        "description": "Data removed during HFP calibration period.",
        "id": 64,
    },
    "PluvioDiagnostic": {
        "description": "Pluvio rainguage sent error diagnostic.",
        "id": 128,
    },
    "SnowDaySignal": {
        "description": "Signal from snow depth sensor too low.",
        "id": 256,
    },
    "TdtTSoil": {
        "description": "Soil temperature too low for TDT to operate correctly.",
        "id": 512,
    }
}
```

### Infill flags ###
Here are the flags for infillng within the COSMOS network:
```
{
    "Linear": {
        "description": "Linear interpolation used to infill gap.",
        "id": 1,
    },
    "AltData": {
        "description": "Alternative data used to infill gap.",
        "id": 2,
    }
}
```


## Network specific ##
As mentioned, the same [core flags](#core-flags) are used across networks. However, as may be clear in the above examples, the [processing flags](#processing-flags) can be both generic, and very network specific. For example, we would not need a `TdtTSoil` QC test for a network that does not deploy TDT sensors (such as FDRI).

For this reason, each set of processing flags are unique to each network.

> **Note**: It would be possible to have single shared processing flags where certain flags are simply not used by particular networks, but we have decided to keep them seperate for neatness.

## Bitwise flag values ##
Bitwise values are used within the [TimeFrame](https://nerc-ceh.github.io/time-stream/api/time_frame.html) object to store flags.

Bitwise values are a set of integers where each value is a power of 2 (1, 2, 4, 8, 16, etc.).
The key feature of bitwise values is that any combination of them results in a unique value.
For example, values 1 + 4 = 5. The value 5 cannot be produced by any other combination of bitwise numbers.
To give another example, the value 13 can only be produced by bitwise values 1 + 4 + 8.

Every flag listed above comes with an `id`. These ids are the bitwise values that a TimeFrame object uses to store the flags, in a simple, low memory way. It is the bitwise values that get writen to s3.

Therefore, in order to translate these interger values back into their semantic meanings, the mappings above must be available. For this reason, the mappings will [live in the metadata](#flag-value-storage) (at time of writing this is **not** the case, they are currently stored in the processing code).

## Flag value storage ##
The flag values are stored as [bitwise values](#bitwise-flag-values). In order to map them back to their meanings, the mappings, e.g. see [QC flags](#quality-control-flags) are to be stored in the metadata, availble for both the processing code and the UI to pull down and use.


## Example ##
Above we saw the example of a TimeFrame object for `SWOUT`:

```
┌─────────────────────────┬───────┬─────────────────┬───────────--────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_CORR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---             ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64             ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═════════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ 126.5 ┆ 0               ┆ 0               ┆ 0             ┆ 0                 │
```

Lets say this data point fails the `Range` QC test, then the `id` (1) is added to the QC flag column.

```
┌─────────────────────────┬───────┬─────────────────┬───────────────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_PR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---           ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64           ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═══════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ 126.5 ┆ 0               ┆ 0             ┆ 1             ┆ 0                 │
```

To illustrate how multiple flags can be added, lets say it also failed the `Samples` (4) test...
```
┌─────────────────────────┬───────┬─────────────────┬───────────────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_PR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---           ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64           ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═══════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ 126.5 ┆ 0               ┆ 0             ┆ 5             ┆ 0                 │
```
The bitwise value of 5, can only be derived from flags 1 + 4, therefore we know exactly which two tests it failed.

The processing code removes values that fail QC tests. This results in the value being set to `null` and the core flad `removed` (8) being added...

```
┌─────────────────────────┬───────┬─────────────────┬───────────────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_PR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---           ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64           ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═══════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ null  ┆ 8               ┆ 0             ┆ 5             ┆ 0                 │
```
Next, the data is sent through infilling. Let's say it receives `Linear` (1) interpolation and gets a new value. This will trigger two new flags; the infill flag **and** the core flag for `estimated` (2)...

```
┌─────────────────────────┬───────┬─────────────────┬───────────────┬───────────────┬───────────────────┐
│ time                    ┆ SWOUT ┆ SWOUT_CORE_FLAG ┆ SWOUT_PR_FLAG ┆ SWOUT_QC_FLAG ┆ SWOUT_INFILL_FLAG │
│ ---                     ┆ ---   ┆ ---             ┆ ---           ┆ ---           ┆ ---               │
│ datetime[μs, UTC]       ┆ f64   ┆ i64             ┆ i64           ┆ i64           ┆ i64               │
╞═════════════════════════╪═══════╪═════════════════╪═══════════════╪═══════════════╪═══════════════════╡
│ 2024-03-08 00:00:00 UTC ┆ 1.56  ┆ 10              ┆ 0             ┆ 5             ┆ 1                 │
```
We now have a dataset that tells us a story...

The core flag of 10 tells us this data value was `removed` (8) and `estimated` (2)
The QC flag tells us the original value failed two tests; `range` (1) and `samples` (4)
And the infill flag tells the current value was created using the `linear` interpolation technique.
