# DP10 Spatial Data System — Task Prioritisation

**Draft — March 2026**

---

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

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Set up PostGIS connection from API | 🟢 Sept | FPM-708 | In progress. Replaces abandoned geoparquet approach. |
| Design PostGIS database structure | 🟢 Sept | FPM-879 | In review. Schema for layer registry: name, type, S3 URL, bounding box, categories, etc. |
| Set up spatial index in PostGIS | 🟢 Sept | FPM-709 | Needed for geospatial querying of layers. |
| Populate PostGIS registry with initial layers | 🟢 Sept | | At least one of each type as proof of concept, then bulk populate with rest of layers (see section 3 below). |

### S3 Storage

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Design production S3 bucket structure | 🟢 Sept | FPM-710 | Ready for doing. Tied to AWS migration. Finalise folder/partition key conventions. |
| Create S3 bucket structure | 🟢 Sept | FPM-710 | Tied to AWS migration. |

### OGC Web Services

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Add WMS endpoint for raster data | 🔵 Mar 27 | | TiTiler WMS extension may suffice for raster. Evaluate OGC compliance. |
| Add WMS/WFS for vector data | 🔵 Mar 27 | | Investigate options. Avoid full GeoServer overhead if possible, but may need. |
| Support OGC API Tiles standard | 🟡 Later | | Newer standard closer to XYZ format TiTiler already uses. |
| STAC catalogue integration | 🟡 Later | | For discoverability in QGIS/ArcGIS. |

---

## 2. Web UI Functionality

*Features needed to make the map viewer functional for the soft launch.*

### Core UI features (soft launch)

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Display legends for raster layers | 🟢 Sept | FPM-837 | Ready for doing. Can hardcode initially, drive from metadata later. |
| Layer opacity controls | 🟢 Sept | FPM-842 | Ready for doing. Essential for overlaying layers. |
| Change basemap | 🟢 Sept | FPM-845 | Ready for doing. Currently hardcoded. Add OS maps, satellite, light, street. |
| Improve layer navigation/panel | 🟢 Sept | FPM-838 | Current design just set up for testing. Needs categories (e.g. region, data type). |
| Configure zoom levels per layer | 🟢 Sept | FPM-733 | Prevent users zooming to irrelevant scales. Related: FPM-899 (min/max zoom). |
| Point record layers with popups | 🟢 Sept | FPM-851 | Click to select, show metadata, link out to timeseries UI / NRFA / EA pages. Needs site info from metadata API. |
| Point value queries from rasters | 🟢 Sept (nice to have) | | Click on raster to see value. TiTiler supports natively, needs API wiring. Has implications for how rasters are stored - will need to be stored as grey-scale rather than colorised COG. Possibly stored both grey-scale (for querying) and colorised rasters (for viewing) |
| 3D terrain visualisation | 🟢 Sept (nice to have) | | Prototype working with deck.gl TerrainLayer. Height exaggeration helps. Performance issues with 50m DEM at national scale. Limit to small layers to start with. |

### Enhanced Viewing (Operational Beta)

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Complex vector data support | 🔵 Mar 27 | FPM-843 | For huge vector datasets that can't be served via geojson. Investigate PostGIS served vector tiles for large datasets (NRFA catchments, river lines)? Or rasterise and serve via WMS? Need for riverlines layer. Use existing NRFA Geoserver WMS feeds for September |
| Suppress 500 errors in console |🔵 Mar 27 | FPM-839 | Not user-facing but important for production. |
| Dynamic colourmap changes | 🟡 Later | | Let users change colourmap on the fly for greyscale rasters. |
| User-chosen vector colours | 🟡 Later | FPM-840 | Nice to have. |

---

## 3. Data Population

*Getting layers processed, uploaded, and visible. Prioritise what's needed for soft launch.*

Each layer may need it's own data processing scripts developed. (e.g. Automate COG conversion, colourmaps, legends, S3 upload).

### Priority Layers for Soft Launch

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| FDRI catchment boundaries | 🟢 Sept | FPM-846 | Existing GeoJSON. Foundation layer. |
| FDRI / COSMOS site locations | 🟢 Sept | | Point records linking to timeseries UI. Point locations taken from FDRI metadata API? |
| River flow gauging stations | 🟢 Sept | FPM-847 | EA/SEPA/NRW APIs. Highlight NRFA stations. Link out. |
| River level stations | 🟢 Sept | FPM-848 | From EA/SEPA/NRW APIs. |
| UKCEH rivers (IRN) | 🟢 Sept | FPM-865 | Complex vector. ~400k features. May need vector tiles or WMS. (dependent on FPM-843). Use NRFA WMS. |
| Elevation (50m DTM) | 🟢 Sept | | Colourised COG. |
| Average annual rainfall | 🟢 Sept | | Existing raster, needs COG conversion. |
| Raingauges | 🟢 Sept | FPM-849 | Point layer from various operators (e.g. EA, Met office, SEPA). |
| NRFA catchment boundaries | 🟢 Sept | | ~1700 overlapping polygons. Complex vector — needs vector tiles. Use NRFA WMS. |
| Land cover map (latest) | 🟢 Sept | FPM-867 | Latest year. Re-use existing EIDC WMS if possible. |
| 1m EA/NRW LiDAR (clipped) | 🟢 Sept | FPM-866 | Clipped to catchments (Chess and Severn) |
| Plynlimon monitoring sites (7 layers) | 🟢 Sept | FPM-859–864 | Flow, AWS, raingauges, soil moisture, groundwater, water quality, daily weather. |

### Second Priority Layers (Operational Beta)

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Land cover map (historical) | 🔵 Mar 27 | | Might be nice to allow users to look back at previous land cover products to look at land cover change. |
| BGS hydrogeology 625k | 🟢 Sept (nice to have) | FPM-869 | Existing raster. Contextual layer. |
| BGS superficial geology | 🟢 Sept (nice to have) | FPM-870 | Existing raster. |
| BGS soil texture | 🟢 Sept (nice to have) | FPM-871 | Existing raster. |
| BGS soil thickness | 🟢 Sept (nice to have) | FPM-872 | Existing raster. |
| BGS boreholes | 🟢 Sept (nice to have) | FPM-856 | UK-wide point data from BGS API. |
| Weather stations (MIDAS) | 🔵 Mar 27 | FPM-873 | Needs processing. Show type metadata on hover. |
| 1m EA/NRW LiDAR (national) | 🔵 Mar 27 | FPM-866 | Large dataset. Probably WMS-based. Check SEPA data for Tweed. |
| Tweed UAV LiDAR DEM + imagery | 🟢 Sept (nice to have) | FPM-857/858 | 2 processed sites. Link DEM/DSM/orthomosaic per flight. |
| CHASM monitoring sites + data | 🔵 Mar 27 | FPM-876–878 | Upper Severn only. TBR, AWS, flow sites. |
| Chess spring locations | 🔵 Mar 27 | FPM-854 | BGS survey. Internal only? |
| BGS geophysical survey lines | 🔵 Mar 27 | FPM-855 | Internal only? |
| Citizen science flow gaugings | 🔵 Mar 27 | FPM-853 | Chess only. Show summary metadata on hover. |
| EA flow gaugings | 🔵 Mar 27 | FPM-852 | Currently blocked. Chess data available, others need requesting. |
| EA water quality monitoring | 🟡 Later | FPM-874 | |
| EA groundwater sites | 🟡 Later | FPM-875 | |
| Land cover plus crops | 🟡 Later | FPM-868 | Restricted - not public. |

---

## 4. Metadata Integration

*Connecting the spatial system to the FDRI metadata service and EIDC catalogue.*

### Minimum Viable (Soft Launch)

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Define minimum metadata per layer type | 🟢 Sept | FPM-99 | Raster: name, S3 URL, legend, bounding box. Vector: name, S3 URL, display fields. Point: name, coord, URLs, dates. |
| Layer categorisation scheme | 🟢 Sept | | Region + data type at minimum. Drives UI navigation panel. |
| Hardcode metadata if needed | 🟢 Sept | | Pragmatic approach: don't wait for full metadata integration. Get layers showing. |

### Full Integration (Operational Beta)

| Task | Target | JIRA | Notes |
|------|--------|------|-------|
| Define what metadata API provides vs PostGIS | 🔵 Mar 27 | | Key architectural question. PostGIS for spatial index + display config; metadata API for dataset descriptions? |
| API reads layer list from metadata service | 🔵 Mar 27 | FPM-98 | Generic geospatial endpoint. Discuss with Epimorphics. |
| Fetch site info from metadata API | 🔵 Mar 27 | FPM-851 | Generic approach for FDRI, COSMOS, NRFA sites. |
| Integrate with EIDC catalogue | 🔵 Mar 27 | | Use catalogue records for certain data layers, e.g. LCM. Link to EIDC pages. |
| Ingestion process for 3rd party layers | 🔵 Mar 27 | | Ingestion process for keeping 3rd party API data (EA, SEPA, Met Office) up to date (as agencies add or remove sites). Similar to timeseries ingester but metadata-only? |

---

## 5. Wider Requirements & Future Work

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
