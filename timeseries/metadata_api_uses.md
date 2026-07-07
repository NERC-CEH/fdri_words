# Uses of the metadata api 

Describes the various endpoints called by the metadata api for the data api and geospatial data api

## dri-data-api

### Networks endpoint

endpoint url: https://dri-data-api.staging.dri.ceh.ac.uk/v1/networks

metadata url:  https://dri-metadata-api.dri.ceh.ac.uk/id/network.json

transformed response: 
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

transformation mapping: 
ID: 
	- @id 
		(splits the returning @id value on / and takes the last item in the split identifier)

### Sites

endpoint: https://dri-data-api.staging.dri.ceh.ac.uk/v1/cosmos/sites

metadata url:  https://dri-metadata-api.dri.ceh.ac.uk/id/network/cosmos.json?_projection=contains.label,contains.comment,contains.identifier,contains.hasGeometry.*

transformed response: 
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

transformation mapping: 

ID: 
	- identifier
Label: 
	- label
Description: 
	- comment
location: 
	hasGeometry.asWKT 
		(Decodes both lat,lon and easting,northing using the point WKT strings)

Variables
----------

endpoint: https://dri-data-api.staging.dri.ceh.ac.uk/v1/cosmos/variables/alic1

metadata url: https://dri-metadata-api.dri.ceh.ac.uk/id/site/cosmos-alic1/_datasets.json?_projection=sourceColumnName,measure(aggregation(prefLabel)),originatingFacility(hasAnnotation(hasValue(value)))&_withView=

transformed response: 
{
  "site_id": "alic1",
  "variables": [
    {
      "id": "http://fdri.ceh.ac.uk/id/dataset/cosmos-alic1-rh_30min_raw",
      "label": "Relative humidity",
      "observedProperty": "Relative humidity",
      "units": "%",
      "sourceColumnName": "RH",
      "statistic": "Mean",
      "resolution": "PT30M",
      "level": "Raw"
    },
  ]
}

transformation mapping: 
	ID
		- @id
	originating facility
		- originatingFacility.hasAnnotation.hasValue.value
	observedProperty
		- observedProperty.prefLabel
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
