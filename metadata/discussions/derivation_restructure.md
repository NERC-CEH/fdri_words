## Getting config data into derivations

Currently only TS datasets are set up as arguments (dependencies) for derivations, e.g. RN needs SWIN, SWOUT etc.
There is no mechanism for other args, e.g. site altitude, soil calibration results, or sensor height.

One issue is that the values are site‑specific, while derivation configs are built around TS definitions. This prevents placing the values directly in derivation metadata. Two pragmatic options:

**Option 1** — treat config values as TS datasets
- Concept: model config items (e.g. sensor height) as time series datasets (one value per timestamp or a stepwise series).
- Pros:
    - Changes (re‑deployments, recalibrations) are captured in the data history.
    - Fits existing TS dependency patterns and can be queried like other datasets.
- Cons:
    - How this TS is derived still requires a new mechanism, i.e. sensor height TS has no dependencies and calculation, it requires a special metadata call to build it. How this is made generic is still a question.
    

**Option 2** — add a "function" argument to derivations
- Concept: derivation configs include a named function (or handler) that fetches site metadata (sensor height, soil calibration, altitude) from the metadata store at runtime.
- Pros:
    - Flexible and lightweight for non‑time‑series metadata.
    - Avoids creating many small TS datasets when values are static or rarely change.
- Cons:
    - Less automatic audit trail than TS datasets (unless functions themselves return versioned values).
    - Requires implementing and maintaining a set of trusted functions and their contracts.

**Option 3** - remove TS definitions!
- Concept: Switch derivation configs to be on dataset (ID) rather than definition. This would be a major change meaning every derived dataset has to individually map its dependencies, e.g. BUNNY-RN needs BUNNY-SWIN etc, SHEEP-RN needs SHEEP-SWIN etc.
- Pros:
    - Complete control over any site specific derivations. E.g. if a site is missing TDT1, we can point it to TDT2 (we currently do not have this requirement). Also note, TS defs do not distinguish between sensors measuring the same thing, e.g. TDT1 and TDT2. This means mapping defs as dependencies means the code must know to expect two options.
    - Would simplify the dependency view that has to map defs to sites.
    - The thinking is that with this, the required values can be returned within the config. I.e. a sparql query can fetch the sensor height and return in a view with the derivation config. (Would need to check this)
    - Would mean we can treat derivation like other processing config
- Cons:
    - Much more dependencies to maintain.
    - Danger of ones getting missed and out of sync
    - Large refactor

**Option 4** - metadata with dataset
- Concept: Config metadata should be linked to the TS dataset it applies to. E.g. Windmaster height is metadata that attached to the WS and WD datasets.
- Cons:
    - Not all configs are dataset specific, e.g. site altitude or soil calibration


Although a major change, option 3 presents a number of benefits and so will discuss if possible with Epimorphics