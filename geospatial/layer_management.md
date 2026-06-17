
# Layer management

Layers in the database can be listed, added or modified using the various endpoints under the `Layer Management` section in the API documentation (see https://dri-geospatial-api.dri.ceh.ac.uk/api/docs) 

## Model names
A few of the layer management endpoints require providing a `model_name`. This is to tell the API which model to list / modify. 

Models which are added / edited using shared endpoints:
- project
- data_format
- data_category_group
- processing_level
- location_type

Models with model-specific endpoints for adding or modifying data:
- source_type
- data_category
- location

## Listing existing models

To view the contents of any models except `Layer`, the `/list_model` endpoint can be used. For example https://dri-geospatial-api.dri.ceh.ac.uk/api/list_model?model_name=project will list all Project model entries available in the database

To list all `Layer` model entries use the `/available_data` endpoint instead. 

## Adding or editing model entries

### Generic models

For those models listed as "generic", new entries can be added using the `/add_model` endpoint. The name of the model needs to be provided, along with the name and the object_key. The name is used for the human readable representation, and the object key should be a unique identifier. 

For example `/add_model?model_name=data_category_group&name=Example%20group&object_key=test` will create a new DataCategoryGroup object with a display name of "Example group" and a unique id of "test".

To edit an existing generic model, use the `/update_model` endpoint. The numeric primary key ID of the model (stored as `id` in the data returned using the /list_model endpoint) must be provided alongside any relevant fields to be changed. For example to edit the name of an existing project, with a primary key ID of 1 the following url would be used: `/update_model?model_name=project&model_id=1&name=Flood%20and%20Drought%20Research%20Infrastructure`. Note that no `object_key` value was provided in order to ensure the existing object value is not modified. 

### Source Type

The source type model is very similar to the core generic model, but contains an additional `base_url` field. The base url is expected to be the name of the base bucket if the source type is S3 (e.g. "s3://ukceh-fdri-staging-geospatial"), or the base metadata api url if the source type is the metadata api (e.g. `https://dri-metadata-api.dri.ceh.ac.uk`). For the base url of any other source types, it is intended to be the basic url from which customisations can be added on a per-layer basis. 

The urls to add or edit a source type model instance are `/add_source_type` and `/update_source_type` respectively

### Data categories
Data categories link to data category group instances to allow similar categories to be grouped together. This means that in addition to the generic endpoint fields of `name` and `object_key` an additional `category_group_key` field is expected. The value of the `category_group_field` is expected to match an existing `object_key` found in the list of available data_category_group model instances. 

Data categories can be created using the `/add_data_category` endpoint and edited using the `/update_data_category` endpoint. When editing an existing data category, the numeric primary key ID of the data_category instance ot be changed must be provided. All other fields are optional, as only those fields with new values submitted will be updated. Everything else will remain the same. 

### Locations

Similar to the data_category model, the each instance of a `location` model has a supporting `location_type` model instance. This allows grouping of the locations into different types, for example the locations "Tweed", "Plynlimon" and "Chess" are all associated with the "river catchment" location type. 

When creating or editing a location, in addition to the generic fields of `name` and `object_key`, a `location_type_key` matching an `object_key` value of an existing `location_type` instance and a boundary geometry must be provided. 
It is easiest to submit boundary data using the documentation endpoints by dragging and dropping a geojson file into the relevant field. Please see the section on [Boundary geometry requirements](#boundary-geometry-requirements). 

The endpoints for adding and editing locations respectively are `/add_location` and `/update_location`

### Layers

Layers can be considered the end product, taking information from all models mentioned previously. Please see the main documentation on the geospatial api design [here](geospatial/geospatial_api_design.md) for information on the individual field requirements.
Where any field requests a "_key", e.g. "project_key", this should refer to the `object_key` value of the corresponding existing model instance. For example `project_key` refers to the object_key of an existing Project instance. 

#### Uploading data
When creating or editing a layer, the supporting source data can be provided in a few ways. These are detailed in the subsections below. 

The endpoints for adding or editing layers are `/add_layer` and `/update_layer` respectively. It is advised to use the docs endpoint to access these as it makes submitting files significantly easier.

Note that when a `_file` field is left blank, the option to `Send empty value` should be unchecked. 

Each layer is expected to have a boundary. Please see the section on [Boundary geometry requirements](#boundary-geometry-requirements) for the data format requirements

##### Raster data stored on S3, served via TiTiler
Required field values: 
- data_format: `vector`
- source_type: `s3`

If the data is a raster with both rendered (colourised) and greyscale (single band) versions available. This can be submitted to be uploaded to S3 by choosing the relevant files in the `raw_source_file` and `colour_source_file` fields. The `raw_source_id` and `colour_source_id` fields should then be left blank. 
Where only one the colourised data is available, both the `raw_source_id` and `raw_source_file` fields should be left blank. 

If legend information is available, this should be submitted as a separate json file. Details on legend formatting can be found [here](#legend-formatting)

#### Geojson data stored on S3
Required field values: 
- data_format: `vector`
- source_type: `s3`

All geojson data is expected to be reprojected into WGS84 before being submitted for upload. 

For geojson data that is to be uploaded to S3, this should be submitted using the `raw_source_file` field. The `raw_source_id`, `colour_source_id` and `colour_source_file` fields should be left blank. 

It is expected that the `legend` and `field_metadata` fields will be also left blank. Please ensure the `send empty value` option is not checked. 

#### Metadata api point locations

Required field values: 
- data_format: `vector`
- source_type: `metadata_api`. Note that the `base_url` for the source type is expected to be the base metadata api url, for example https://dri-metadata-api.dri.ceh.ac.uk

Where a layer needs to load vector point information from the metadata api, the `raw_source_id` should be specified as the part of the url returning the required information, without the base metadata api. For example `/id/network/cosmos.json?_projection=contains.label,contains.comment,contains.identifier,contains.hasGeometry.*,contains.operatingPeriod.*,contains.altitude`. The `raw_source_file`, `colour_source_id` and `colour_source_file` fields should all be left blank

The `legend` field should also be left blank, but the `field_metadata` needs to be configured to allow the API to decode the expected data from the metadata api's response. Please see [here](#field_metadata) for information on the contents of the `field_metadata` field should be configured. 

### Field metadata

The field_metadata field is designed to store a list of dictionaries, with each dictionary containing a configuration detailing how a specific field from the metadata api should be decoded. 
Each dictionary is expected to have the following 4 fields: 
- display_label : This is the label to be used in the UI for displaying the field information
- key: This is the unique identifier the decoded metadata information will be stored under.
- field_keys: This is a list of dictionaries, each referring to a specific metadata field.
- data_type: The data type of the final decoded metadata api value

#### Field keys


Metadata api response data can often be stored in a nested format. As such each level of nesting needs it's own instructions to be able to decode the information. Each `field_keys` dictionary entry is expected to have two keys. 
- `key`: This should be the key in the metadata api response to be read
- 'type': This indicates the type of data returned when the metadata key's value is returned. There are several possible `types` supported
  - `value`: Used to represent returning the raw value, regardless of it's data type
  - 'list: Indicates that the returned value should be extracted from a list. If this is used, then an additional `index` field should also be provided to inform the API which index in the list should be chosen. For example `[{"key": "comment", "type": "list", "index": 0}]`
  - `wkt_list`: This is a custom type to be used only for the `hasGeometry` metadata api field. It is designed to handle the point coordinate extraction from multiple possible WKT strings, each in a different coordinate system.

Where `hasGeometry` is part of the metadata response, this is an example configuration entry:

```
{
    "display_label": "Location",
    "key": "geometry",
    "field_keys": [{"key": "hasGeometry", "type": "wkt_list", "index": None}],
    "data_type": "string",
}
```

##### Example 
For example, the start and end date information is returned from the metadata api as 

```
 "operatingPeriod": {
     "@id": "http://fdri.ceh.ac.uk/id/site/cosmos-eustn#operating-period",
         "@type": [
              {
                "@id": "http://purl.org/dc/terms/PeriodOfTime"
              }
            ],
    "endDate": "2099-12-31",
    "startDate": "2016-03-31T16:00:00
}
```
To instruct the API to be able to decode this the following `field_metadata` entry is used

```
{
    "display_label": "Start Date",
    "key": "start_date",
    "field_keys": [{"key": "operatingPeriod", "type": "value"}, {"key": "startDate", "type": "value"}],
    "data_type": "date",
}
```
The `field_keys` entry has two items. It is intended that this represents the nested structure of the response to be decoded, and will be processed in order. 
In this case, the first item (`{"key": "operatingPeriod", "type": "value"}`) will return the following information:
```
{
     "@id": "http://fdri.ceh.ac.uk/id/site/cosmos-eustn#operating-period",
         "@type": [
              {
                "@id": "http://purl.org/dc/terms/PeriodOfTime"
              }
            ],
    "endDate": "2099-12-31",
    "startDate": "2016-03-31T16:00:00
}
```
And then the second item in the field_keys list (`{"key": "startDate", "type": "value"}`), allows the final start date value to be extracted as the "startDate" key is now available at the top level of the dictionary. 

## Legend formatting

The `legend` field is designed to store the legend configuration. At the top level there should be two fields:
- `type`: Defines the type of the legend. Currently only `range` is supported.
- `values`: Is a list of dictionaries, with each dictionary containing a single legend entry

### Range legends
The `range` legend type is used to represent colourised rasters where each colour band contains a range of values (and the colour will change accordingly across that range). 

An example of a complete legend is shown below. Both `min` or `max` fields are expected to have the same structure, comprising of these two fields:
- `label` which is used to represent the min or max bounds respectively
- `colour` which contains a list of three items, representing the [red, green, blue] values respectively. It is expected that each colour value is within the range of 0-255 inclusive.

The boundary format of the min - max range can be represented as `min > x <= max`. 

```
{
                "type": "range",
                "values": [
                    {
                        "min": {"label": 289.97, "colour": [51, 51, 153]},
                        "max": {"label": 291.61, "colour": [14, 126, 228]},
                    },
                    {
                        "min": {"label": 291.61, "colour": [14, 126, 228]},
                        "max": {"label": 293.25, "colour": [1, 188, 148]},
                    },
                    {
                        "min": {"label": 293.25, "colour": [1, 188, 148]},
                        "max": {"label": 294.9, "colour": [85, 221, 119]},
                    },
                    
                ],
            },
```

## Boundary geometry requirements

All boundaries must comprise of a single Polygon geometry, reprojected into WGS84. It is advised to simplify the polygon as much as is sensible in order to reduce the number of unnecessary vertices. However the boundary should not be simplified to the extent that it misrepresents the area it is intended to cover. 
