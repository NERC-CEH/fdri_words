# DP10 Spatial Data System — Task Prioritisation

**Updated — June 2026**

---

Useful links: 
- Documentation: https://github.com/NERC-CEH/fdri_words/blob/main/geospatial/geospatial_api_design.md
- MapLayers spreadsheet: https://cehacuk.sharepoint.com/:x:/r/sites/FDRI-WP2Digital/_layouts/15/Doc.aspx?CID=64c5c33c-f41c-d5a9-3dcd-7009c147a889&sourcedoc=%7B459276C1-A106-4112-AD73-EA8BE04466EF%7D&file=Map%20layers.xlsx&action=default&mobileredirect=true

## Milestones

**September 2026 (Soft Launch):** Working prototype of the spatial data system with a functional public map viewer. A selection of key layers viewable and navigable. Metadata and layer registry can be bootstrapped/hardcoded. Demonstrates the concept and core data, but rough edges are acceptable.

**March 2027 (End of Year — Y3 Objective):** Operational beta spatial data system supporting map visualisation of FDRI data, populated with consistently stored spatial layers, and integrated with metadata systems. Limited but functional UI with working layer list and layer rendering. OGC web services progressed but not necessarily complete.

### Priority Key

| Label | Meaning |
|-------|---------|
| 🟢 **Sept** | Target for September 2026 soft launch prototype |
| 🔵 **Mar 27** | Target for March 2027 operational beta |
| 🟡 **Later** | Future / nice-to-have / dependent on other work |

---

## 1. Infrastructure & Architecture

*Foundation work that everything else depends on.*

### PostGIS Layer Registry

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Set up PostGIS connection from API | 🟢 Sept | FPM-708 | In progress | Replaces abandoned geoparquet approach. |
| Design PostGIS database structure | 🟢 Sept | FPM-879 | Ready for deployment | Schema for layer registry: name, type, S3 URL, bounding box, categories, etc. |
| Set up spatial index in PostGIS | 🟢 Sept | FPM-709 | Ready for deployment | Needed for geospatial querying of layers. |
| Populate PostGIS registry with initial layers | 🟢 Sept | N/A | In progress | At least one of each type as proof of concept, then bulk populate with rest of layers (see section 3 below). A spreadsheet has been produced listing all layers to go into the database along with the relevant postgis metadata |

### S3 Storage

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Design production S3 bucket structure | 🟢 Sept | FPM-710 | Ready for deployment |. Tied to AWS migration. Finalise folder/partition key conventions. API modified to automatically upload data to the correct S3 structure |
| Create S3 bucket structure | 🟢 Sept | FPM-710 | Done | Tied to AWS migration. The geospatial API has been modified to automatically upload data to the correct S3 structure |

### OGC Web Services

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Add WMS endpoint for raster data | 🔵 Mar 27 | | Not started |TiTiler WMS extension may suffice for raster. Evaluate OGC compliance. |
| Add WMS/WFS for vector data | 🔵 Mar 27 | | Not started | Investigate options. Avoid full GeoServer overhead if possible, but may need. |
| Support OGC API Tiles standard | 🟡 Later | | Not started | Newer standard closer to XYZ format TiTiler already uses. |
| STAC catalogue integration | 🟡 Later | | Not started | For discoverability in QGIS/ArcGIS. |

---

## 2. Web UI Functionality

*Features needed to make the map viewer functional for the soft launch.*

### Core API features (soft launch)

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Add IP filtering | 🟢 Sept | FPM-1086 | Ready for doing |Needed to hide the layer management router used for editing the postgis database. |

### Core UI features (soft launch)

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Display legends for raster layers | 🟢 Sept | FPM-837 | Done | Legends extracted from postgis database |
| Layer opacity controls | 🟢 Sept | FPM-842 | Done | Essential for overlaying layers. |
| Change basemap | 🟢 Sept | FPM-845 | Ready for doing. | Currently hardcoded. Add OS maps, satellite, light, street. Consider licencing, costs etc. |
| Improve layer navigation/panel | 🟢 Sept | FPM-838 | Done | Likely to require some fine tuning once lots of layers available in postgis |
| Configure zoom levels per layer | 🟢 Sept | FPM-733 | Invalid | Handled by deck.gl, no longer required. Prevent users zooming to irrelevant scales. Related: FPM-899 (min/max zoom). |
| Point record layers with popups | 🟢 Sept | FPM-851 | In progress| Click to select, show metadata, link out to timeseries UI / NRFA / EA pages. Needs site info from metadata API. |
| Support WMS layers from the catalogue | 🟢 Sept | FPM-1085 | Ready for doing | To support the backup plan of rendering the NRFA catchments and River lines data using WMS from the data catalogue | 
| Point value queries from rasters | 🟢 Sept (nice to have) | FPM-1017 | Ready for doing | Click on raster to see value. TiTiler supports natively, needs API wiring. Has implications for how rasters are stored - will need to be stored as grey-scale rather than colorised COG. Possibly stored both grey-scale (for querying) and colorised rasters (for viewing) |
| 3D terrain visualisation | 🟢 Sept (nice to have) | FPM-1084 | Ready for doing | Prototype working with deck.gl TerrainLayer. Height exaggeration helps. Performance issues with 50m DEM at national scale. Limit to small layers to start with. |


### Enhanced Viewing (Operational Beta)

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Complex vector data support | 🔵 Mar 27 | FPM-843 | Not started | For huge vector datasets that can't be served via geojson. Investigate PostGIS served vector tiles for large datasets (NRFA catchments, river lines)? Or rasterise and serve via WMS? Need for riverlines layer. Use existing NRFA Geoserver WMS feeds for September |
| Suppress 500 errors in console |🔵 Mar 27 | FPM-839 | Not started |  Not user-facing but important for production. |
| Dynamic colourmap changes | 🟡 Later | | Not started | Let users change colourmap on the fly for greyscale rasters. |
| User-chosen vector colours | 🟡 Later | FPM-840 | Done | Nice to have. |

---

## 3. Data Population

*Getting layers processed, uploaded, and visible. Prioritise what's needed for soft launch.*

Each layer may need it's own data processing scripts developed. (e.g. Automate COG conversion, colourmaps, legends, S3 upload).

### Priority Layers for Soft Launch

| Task | Target | JIRA | Current Status | Notes | Data source | Processing requirements |
|------|--------|------|----------------|-------|-------------|-------------------------| 
| FDRI catchment boundaries | 🟢 Sept | FPM-846 | Not started | Existing GeoJSON. Foundation layer. | Geojson | Will need uploading to S3 and adding to PostGIS. May be stored as "Locations" |
| FDRI / COSMOS site locations | 🟢 Sept | | Not started | Point records linking to timeseries UI. Point locations taken from FDRI metadata API? | Metadata API | Needs entry adding to postgis |
| River flow gauging stations | 🟢 Sept | FPM-847 |  Not started |EA/SEPA/NRW APIs. Highlight NRFA stations. Link out. | Metadata API | Needs entries adding to postgis | 
| River level stations | 🟢 Sept | FPM-848 |  Not started |From EA/SEPA/NRW APIs. |  Metadata API | Needs entries adding to postgis | 
| UKCEH rivers (IRN) | 🟢 Sept | FPM-865 |  Not started |Complex vector. ~400k features. May need vector tiles or WMS. (dependent on FPM-843). Use NRFA WMS. | ? | ? |
| Elevation (50m DTM) | 🟢 Sept | |  Not started | Colourised COG. | Needs convert_to_cog script + raster_boundary script |
| Average annual rainfall | 🟢 Sept | |  Not started |Existing raster, needs COG conversion. | Colourised COG. | Needs convert_to_cog script + raster_boundary script |
| Raingauges | 🟢 Sept | FPM-849 | Not started | Point layer from various operators (e.g. EA, Met office, SEPA). | Metadata API | Needs entries adding to postgis | 
| NRFA catchment boundaries | 🟢 Sept | | Not started | ~1700 overlapping polygons. Complex vector — needs vector tiles. Use NRFA WMS. | WMS | Needs simplifying to make nested boundaries visible. |
| Land cover map (latest) | 🟢 Sept | FPM-867 |  Not started | Latest year. Re-use existing EIDC WMS if possible. | WMS | Reliant on FPM-1085 | 
| 1m EA/NRW LiDAR (clipped) | 🟢 Sept | FPM-866 |  Not started | Clipped to catchments (Chess and Severn) | S3 COG |  Needs convert_to_cog script + raster_boundary script |
| Plynlimon monitoring sites (7 layers) | 🟢 Sept | FPM-859–864 | Not started | Flow, AWS, raingauges, soil moisture, groundwater, water quality, daily weather. | Metadata API | Needs entries adding to postgis | 

### Second Priority Layers (Operational Beta)

| Task | Target | JIRA | Current Status | Notes | Data source | Processing requirements |
|------|--------|------|----------------|-------|-------------|-------------------------| 
| Land cover map (historical) | 🔵 Mar 27 | |  Not started | Might be nice to allow users to look back at previous land cover products to look at land cover change. | S3 COG | Needs convert_to_cog script + raster_boundary script |
| BGS hydrogeology 625k | 🟢 Sept (nice to have) | FPM-869 |  Not started | Existing raster. Contextual layer. | S3 COG | Needs convert_to_cog script + raster_boundary script |
| BGS superficial geology | 🟢 Sept (nice to have) | FPM-870 |  Not started | Existing raster. | S3 COG | Needs convert_to_cog script + raster_boundary script |
| BGS soil texture | 🟢 Sept (nice to have) | FPM-871 | Not started | Existing raster. | S3 COG | Needs convert_to_cog script + raster_boundary script |
| BGS soil thickness | 🟢 Sept (nice to have) | FPM-872 | Not started | Existing raster. | S3 COG | Needs convert_to_cog script + raster_boundary script |
| BGS boreholes | 🟢 Sept (nice to have) | FPM-856 | Not started | UK-wide point data from BGS API. | Metadata API | Needs entry adding to postgis | 
| Weather stations (MIDAS) | 🔵 Mar 27 | FPM-873 | Not started | Needs processing. Show type metadata on hover. | Metadata API | Needs entry adding to postgis | 
| 1m EA/NRW LiDAR (national) | 🔵 Mar 27 | FPM-866 | Not started | Large dataset. Probably WMS-based. Check SEPA data for Tweed. | S3 COG | Needs convert_to_cog script + raster_boundary script |
| Tweed UAV LiDAR DEM + imagery | 🟢 Sept (nice to have) | FPM-857/858 | Not started | 2 processed sites. Link DEM/DSM/orthomosaic per flight. | S3 COG | Needs convert_to_cog script + raster_boundary script |
| CHASM monitoring sites + data | 🔵 Mar 27 | FPM-876–878 | Not started | Upper Severn only. TBR, AWS, flow sites. | Metadata API | Needs entry adding to postgis | 
| Chess spring locations | 🔵 Mar 27 | FPM-854 | Not started | BGS survey. Internal only? | | |
| BGS geophysical survey lines | 🔵 Mar 27 | FPM-855 | Not started | Internal only? | | |
| Citizen science flow gaugings | 🔵 Mar 27 | FPM-853 | Not started | Chess only. Show summary metadata on hover. | Metadata API | Needs entry adding to postgis | 
| EA flow gaugings | 🔵 Mar 27 | FPM-852 | Not started | Currently blocked. Chess data available, others need requesting. | Metadata API | Needs entry adding to postgis | 
| EA water quality monitoring | 🟡 Later | FPM-874 | Not started | | Metadata API | Needs entry adding to postgis | 
| EA groundwater sites | 🟡 Later | FPM-875 | Not started | | Metadata API | Needs entry adding to postgis | 
| Land cover plus crops | 🟡 Later | FPM-868 | Not started | Restricted - not public. |

---

## 4. Metadata Integration

*Connecting the spatial system to the FDRI metadata service and EIDC catalogue.*

### Minimum Viable (Soft Launch)

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Define minimum metadata per layer type | 🟢 Sept | FPM-99 | Not started | Concentrate on what metadata that scientists/end users want to see in the UI. This metadata should sit in the metadata service / EIDC catalogue rather than PostGIS |
| Layer categorisation scheme | 🟢 Sept | | Not started | Region + data type at minimum. Drives UI navigation panel. |
| Define dataset series (collections) and how to access from metadata API | 🟢 Sept | | Needs talks with Epimorphics. Fall back to hardcoding lists if necessary. |
| Hardcode metadata if needed | 🟢 Sept | | Not started |Pragmatic approach: don't wait for full metadata integration. Get layers showing. |
| Integrate with EIDC catalogue | 🟢 Sept | | Not started | Link to EIDC catalogue pages from our UI where available. |

### Full Integration (Operational Beta)

| Task | Target | JIRA | Current Status | Notes |
|------|--------|------|----------------|-------|
| Define what metadata API provides vs PostGIS | 🔵 Mar 27 | | Not started | Key architectural question. PostGIS for spatial index + display config; metadata API for dataset descriptions? |
| API reads layer list from metadata service | 🔵 Mar 27 | FPM-98 | Not started | Generic geospatial endpoint. Discuss with Epimorphics. |
| Fetch site info from metadata API | 🔵 Mar 27 | FPM-851 | Not started | Generic approach for FDRI, COSMOS, NRFA sites. |
| Ingestion process for 3rd party layers | 🔵 Mar 27 | | Not started | Ingestion process for keeping 3rd party API data (EA, SEPA, Met Office) up to date (as agencies add or remove sites). Similar to timeseries ingester but metadata-only? |
| Further integration with EIDC catalogue | 🔵 Mar 27 | | Not started | Get more datasets in the catalogue and determine what other bits of metadata we want to pull through from here. |

---

## 5. National LiDAR dataset and notebooks

### Dataset publication

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Finalise supporting documentation | 🟢 Apr 26 | | Finalise detail, decide on whether notebooks will be referenced in docs |
| Publish dataset | 🟢 May 26 | | Need to given EIDC sufficient time to ingest. Process started by Michael T |

### Notebook publication

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Summarise changes to notebooks | 🟢 Apr 26 | | MF |
| Decide consistent approach to notebook style, format, storage | 🟢 Apr 26 | | Discuss with gridded data work. Logos in notebooks, attribution, github repo? |
| Implement updates | 🟢 May 26 | |  |
| Publish to zenodo | 🟢 May 26 | |  |
| Link to dataset catalogue record | 🟢 June 26 | | |

---

## 6. Wider Requirements & Future Work

### Access Control

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Determine which layers are restricted | 🔵 Mar 27 | | Some data (springs, LCM+crops, internal analysis) not public. |
| Implement authentication for restricted layers | 🔵 Mar 27 | | PostGIS could support role-based access. May depend on layer count/complexity. |

### Exploratory / Future

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Drape orthomosaic over DEM in 3D | 🟡 Later | | Prototype feasible. Needs metadata to pair DEM/DSM/orthomosaic per flight. |
| Hillshade raster representation | 🟡 Later | | May be more useful than 3D for some contexts. |
| External user photo/comment uploads | 🟡 Later | | QField / QFieldCloud option raised. Citizen engagement. |
| Editable contextual layers (WFS-T) | 🟡 Later | | From Rafa's plan. For field teams updating site locations. |
| Land cover explorer widget integration | 🟡 Later | | Reuse DRI work on WMS layer selection widgets. |
