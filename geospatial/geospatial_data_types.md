# Geospatial Data Types for the UI

The data to be displayed in the UI can be split into a number of different standardised types

## Pre-colourised raster data served via WMS

This is raster data which has had colourisation applied and is stored in a geospatial database (such as the EIDC map
server) as a series of pre-calculated tiles.

### WMS

Raster tile data served via WMS is typically png images showing a part of the raster for the requested bounding box and EPSG code. For example the following url requests a river river data for the area

https://example.com/geoserver/wms/river_vectors?service=WMS&request=GetMap&layers=river_vectors%3AIRN_riverLine&styles=&format=image%2Fpng&transparent=true&version=1.1.1&id=IRN&width=256&height=256&srs=EPSG%3A3857&bbox=-78271.51696402048,6711782.579664759,-58703.637723015374,6731350.458905762

## Pre-colourised raster data served via TiTiler

This is raster data which has been converted into an RGBA format raster, before being converted into a COG formatted
raster.

RGBA rasters are expected to contain 4 bands representing red, green, blue and alpha bands respectively. Each band should
have a byte data type (8 bit unsigned integer), which limits values from 0-255 inclusive. This allows easy conversion
into the .png tile format produced by TiTiler

Cloud Optimised GeoTIFF (COG) files are designed to be more performant when hosted on a file server such as S3, allowing
on-the-fly tiling of the data using libraries such as TiTiler.

The data is typically reprojected into EPSG 3857 in order to natively support the WebMercatorQuad method used by TiTiler
for fetching raster tiles.

### Legend format

As the raster has been pre-colourised, a legend will be required in order to be able to inform users what is represented
by each colour. This should stored alongside the raster

The format of the legend should be a list of dictionaries. Each dictionary has two keys
- `value` : This will be used to show the value of the raster at that colour. It can be a single number (integer or float) 
  or a string (e.g. "100-200")
- `colour`: This is the RGBA representation of the colour. Note that the alpha value should be 255 as the opacity of the
  layer can be controlled in the UI itself.

For example:

```
[
    {
        "value": 123,
        "colour": [255,0,255,255]
    }
]
```

## Greyscale raster data served via TiTiler

This is single-band raster data which has been converted into a COG formatted raster. Colourisation is then applied by
TiTiler when raster tiles are requested by the UI.

For the same reasons as the colourised raster served via TiTiler, the raster should be reprojected to EPSG 3857.

The benefit of serving the greyscale data directly, means that it is easily possible to query the point value of a
location within the raster. However, it does come with a performance cost, as there is more processing required by 
TiTiler in order to be able to generate the raster tiles on the fly. It also makes it harder to generate a legend as
the colourmap application logic is located within TiTiler.

## Complex vector data served via vector tiles

Where vector data is too large to easily be served as a geojson file via API, but the ability to select or interact
with features from that layer is still required, it should be served as vector tiles. The method by which the vector 
tiles are served and stored is still in development.


## Complex vector data served via WMS

As an alternative to the above, it is possible to serve the vector data via WMS instead. 


## Simple vector data

Where vector data is small enough to send as a geojson via API, it can be read from S3 and served directly to the UI.
The vector data should be stored as a single geojson file reprojected into WGS84 (EPSG 4326)

## Point record layers

Point record layers are an extension of the simple vector data format, but refer specifically to vector data which 
contains a series of points, each of which links to another dataset or supplementary data. For example, a geojson 
file containing locations of FDRI sites, each of which links to the timeseries UI for that site. 

Each feature should contain at least the following properties:
- id: A unique ID to represent the feature
- name: The display name to show in a tooltip for the feature
- description: A description of what the point represents. This may be empty
- url: The url to associate with the point, and to open in a new tab when the user clicks on it. 

It is likely that a lot of these layers will be generated on the fly from external API data, such as the FDRI metadata 
API serving a list of COSMOS, FDRI and NRFA sites.
