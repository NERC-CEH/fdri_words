### 2025.05.28 API Planning

We discussed the endpoints we might want to create in a combined data/metadata api.

Endpoints to create:
- /v1/networks -> list of networks cosmos/fdri/etc
- /v1/fdri/sites/(x) -> list of sites + variable info resolution, location
- /v1/fdri/variables/(x) -> sites, units, resolution, process_level
- /v1/fdri/data?sites=[]&start_date=x&end_date=y&resolution=z&dataset=aa&&aggregation=bb
- /v1/fdri/data_availability (maybe covered in /variables)
- /v1/fdri/datasets -> CHESS_catchment_rainfall = list of ts ids
- /v1/fdri/timeseries_ids -> precip_1min_raw_bunny

![image](https://github.com/user-attachments/assets/ea7a77c5-86c5-4c47-be7c-39e9909eb130)
