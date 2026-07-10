# Uses of the metadata api 

Describes the various endpoints called by the metadata api for the data api and geospatial data api

## dri-data-api

### Networks endpoint

##### Endpoint url
https://dri-data-api.staging.dri.ceh.ac.uk/v1/networks

##### Metadata url
https://dri-metadata-api.dri.ceh.ac.uk/id/network.json

##### Transformed response
```
[
  {
    "id": "cosmos"
  },
  {
    "id": "nrfa"
  },
  {
    "id": "fdri"
  },
  {
    "id": "ea-manual-sites"
  },
  {
    "id": "rca"
  },
  {
    "id": "nmdb"
  }
]
```

##### Transformation mapping

ID 
- @id (splits the returning @id value on / and takes the last item in the split identifier)

### Sites endpoint

##### Endpoint url
https://dri-data-api.staging.dri.ceh.ac.uk/v1/cosmos/sites

##### Metadata url
https://dri-metadata-api.dri.ceh.ac.uk/id/network/cosmos.json?_projection=contains.label,contains.comment,contains.identifier,contains.hasGeometry.*

##### Transformed response
```
{
  "sites": [
    {
      "id": "ALIC1",
      "label": "Alice Holt",
      "location": {
        "latitude": "",
        "longitude": "",
        "easting": "",
        "northing": ""
      },
      "description": "This is one of the few COSMOS-UK sites located in woodland; in this case the Alice Holt Forest managed by the Forestry Commission and situated in the South Downs National Park. Alice Holt is also one of the main research stations of Forest Research. The COSMOS-UK instrumentation is co-located with monitoring equipment operated by Forest Research that contributes to FLUXNET and the Environmental Change Network, in an area of broadleaf trees and scrub."
    },
  ]
}
```

##### Transformation mapping

ID
- identifier
  
Label
- label
  
Description
- comment
  
Location
- hasGeometry.asWKT (Decodes both lat,lon and easting,northing using the point WKT strings)

Variables
----------

##### Endpoint url
https://dri-data-api.staging.dri.ceh.ac.uk/v1/cosmos/variables/alic1

##### Metadata url
https://dri-metadata-api.dri.ceh.ac.uk/id/site/cosmos-alic1/_datasets.json

##### Transformed response
```
{
  "site_id": "alic1",
  "variables": [
    {
      "id": "http://fdri.ceh.ac.uk/id/dataset/cosmos-alic1-rh_30min_raw",
      "label": "Relative humidity",
      "units": "%",
      "sourceColumnName": "RH",
      "statistic": "Mean",
      "resolution": "PT30M",
      "level": "Raw"
    },
  ]
}
```

##### Transformation mapping
ID
- @id

label
- title

units
- measure.hasUnit.@id

statistic
- measure.aggregation.prefLabel

resolution 
- measure.periodicity

sourceColumnName
- sourceColumnName

processingLevel
- processingLevel.prefLabel	


## dri-geospatial-api

### Transformation and url used for extracting locations from the metadata api
Note that the individual metadata api urls will likely vary slightly per layer, but the base format and required fields will be the same. The example below is for the cosmos network.

##### Metadata url
https://dri-metadata-api.dri.ceh.ac.uk/id/network/cosmos.json?_projection=contains.label,contains.comment,contains.identifier,contains.hasGeometry.*,contains.operatingPeriod.*,contains.altitude

##### Transformed response (returned as a geojson)
```
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -3.905963,
                    50.773479
                ]
            },
            "properties": {
                "name": "North Wyke",
                "description": "This site is a Rothamsted Research farm where scientists investigate the impact of agriculture on the land and atmosphere. The field where the COSMOS-UK site is located was a grassland with grazing livestock until 2019. Since then it has been used for arable crop production.",
                "altitude": 146.0,
                "start_date": "2014-10-16T09:00:00",
                "end_date": "2099-12-31"
            }
        },
    ]
}
```

##### Transformation mapping

Name
- label

Description
- comment

Altitude
- altitude

Start date
- operatingPeriod.startDate

End date
- operatingPeriod.endDate

Location
- hasGeometry.asWkt (uses shapely.wkt.loads to read the WGS84 point coordinate)
