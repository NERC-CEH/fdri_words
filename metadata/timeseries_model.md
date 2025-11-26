## Dataset / variable levels

#### Property
**Concept**: The type of variable being measured.
**Example**:
- Code: TEMP
- Name: Temperature
- URL: https://dri-metadata-api.staging.eds.ceh.ac.uk/ref/common/property/temperature


#### Parameter
**Concept**: The variable being measured with context. This can include height / depth.
This is refered to as a "*variable*" in the metadata.
**Example**: 
- Code: TEMP_SOIL_10
- Name: Soil temperature (at 10cm)
- URL: https://dri-metadata-api.staging.eds.ceh.ac.uk/ref/common/cop/temp_soil_10


#### Timeseries Definition
**Concept**: The blue print of a dataset for a particular parameter. Includes resolution, process level and can include height / depth. Does NOT include site.
This is refered to as a "*time-series*" in the metadata.
**Example**: 
- Code: TDT_TSOIL_10_30MIN_RAW
- Name: Soil temperature (at 10cm) 30min raw
- URL: https://dri-metadata-api.staging.eds.ceh.ac.uk/ref/cosmos/time-series/tdt_tsoil_10_30min_raw


#### Timeseries ID
**Concept**: Reference to an actual dataset. Site and sensor specific. Is always a tpye of *time-series*.
This is refered to as a "*dataset*" in the metadata.
**Example**: 
- Code: COSMOS-BALRD-TDT1_TSOIL_30MIN_RAW
- Name: Soil temperature (at 10cm) 30min raw at Bunny Park
- URL: https://dri-metadata-api.staging.eds.ceh.ac.uk/id/dataset/cosmos-bunny-tdt1_tsoil_30min_raw

