# Suggestions for refactoring dri-ingestion

1. Make **APIManager interface for ea, sepa and nmdb** networks. Can include the following **abstract methods**:
    - `__init__` to include hostname, ingestion_environment and logger.info
    - `_make_api_call`. Can result be the same for all networks? Either str or response.modles.Response
    - `date_range_parameters`: why is this a static method only for nmdb? Can this be made consistent?
    - `get_data`: can `get_reading` from ea, `get_data` from nmdb and `get_timeseries` from sepa be combined to one, consistent, abstract method?
    - `get_stations`: can `get_stations_for_measure` from ea, and `get_stations_for_timeseries_name_and_station_parameter_name` from sepa be combined to one, consistent, abstract method? 
       How can this be consolidated with `get_sites` from `nmdb_lookup.py`? The former are in the individual network folders in the `api_manager.py` files, whereas the latter is in `metadata_api/models/nmdb_lookup.py`
       Should all of these be in metadata_api rather than APIManager? Should these all use MetadataRouter.fetch_sites?
       Should all `get_stations`/`get_sites` use a 'transform function'? Currenly only in nmdb/nrfa lookup. Is this convention used in other repos?
2. Make `nmdb_lookup.py` and `nrfa_lookup.py` more consistent .
   Unless nmdb's `get_sites` is moved elsewhere to be consistent with ea `get_stations_for_measure` and sepa's `get_stations_for_timeseries....`, then `nmdb_lookup.py` may become redundant.
3. Can `<network>-env.cfg` and `Config.py` files be made more consistent in format across networks? Is it worth considering an interface for `Config.py`? Combine this with `config_factorires.py`?
4. In `metadata.py` for different networks, can the '`column_types`' be named more consistently?
5. For `ingester.py` across different networks:
    - Does `ingester.py` for nmdb network require `IngressData` and `ValidData` classes like other networks have in their ingesters? Are these classes that can be shared across networks?
    - Can the `NRFAFileIngester` class be renamed to `NRFAIngester`, as for other networks, or do we need to distinguish 'file ingesters' and 'metadata ingesters'?
    - Make variable names for e.g. `MetaDataRouter` in ingester `__init__`s consistent.
    - add another interface layer to ingesters, e.g.: 
      
      ingester_interface
      -> sqs_interface
          -> sepa, cosmos, fdri
      -> non-sqs_interface
          -> nmdb, nrfa
      
    - include some basic implementation for `start`, `dedupe`, `validate`, `writer` methods in `integester_interface.py` to reduce duplication in different network ingester implementations.
      - Make the variable names in these methods across different networks more consistent where possible. For example, make `sites` v. `stations` consistent.
      - Make list v dict outputs consistent for same methods across networks
      - Dedupe may not need to be an abstract method. Looks like this is always implemented in the same way.
  6. Can `convert_to_dataframe` and `append_dataframes_with_update` be put in e.g. `utils` and shared across different networks?
  7. `fetch_batches` is used as a method name in both `metadata_api/batches` and in `metadata_api/metatdata_ruoter`. Perhaps rename one or consolidate?
  8. Can those related to nrfa be grouped better? e.g. ea and sepa grouped inside the nrfa folder?
  9. Similarly, can phenocam be grouped with cosmos somehow, or does it need to be treated separately with some shared classes with cosmos?
  10. Can any of `parquet.py`, `schema.py` have shared interfaces/abstract methods?
  11. Perhaps change sqs folder structure so that their are individual folders for `fdri` and `cosmos`, each with their own scheme? 
      This is more similar to the non sqs file structure, rather than both schema being saved in a 'schemas' folder.
  
      
  Finally...**update tests** to reflect any changes!
