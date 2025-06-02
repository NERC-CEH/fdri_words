### Data Storage

We are currently storing all our timeseries data in parquet files on s3, this has it's advantages and works really well for read only data. For the ingestion we have had to add some hacks to avoid horizontal scaling, and it's not great having to read an entire parquet file into memory just to append a single row to the bottom of it when new data comes in (parquet files can't be updated).

On the API we have also seen a number of issues with parquet and have had to create a custom duckdb connection pool to use parquet/duckdb in an API.

We are now wanting to start writing processed data which we already know will require many updates and it would be nice to not have to force processing to only happen sequentially to avoid overwriting data.

Because of the above we have been considering alternative data storage solutions for the timeseries product.

#### Solutions we investigated
- Relational database
	- Pro: Everybody understands them very well
	- Pro: Standard for timeseries data
	- Con: Maintenance
	- Con: Costs more than s3
- S3 table buckets
	- Pro: Supports "updates"
	- Con: Not mean for our small scale
	- Con: Complicated
	- Con: Very slow for small queries (queues queries and produces objects on s3)
- CSV
	- Pro: super simple
	- Con: Con's are the same as parquet
- Iceberg/DuckLake
	- Con: s3 table buckets are managed iceberg


![image](https://github.com/user-attachments/assets/5a8fbde9-afe5-430a-896e-dbe587892541)
