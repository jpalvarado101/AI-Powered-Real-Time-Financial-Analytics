import duckdb
import pandas as pd

# Connect to DuckDB (creates a local file-based DB)
con = duckdb.connect("local_snowflake.db")

# Load cleaned data from Parquet (produced by the ETL pipeline)
df = pd.read_parquet("data/stock_data_cleaned.parquet")

# Store the data into DuckDB (simulate Snowflake table)
con.execute("DROP TABLE IF EXISTS stock_data;")
con.execute("CREATE TABLE stock_data AS SELECT * FROM df")

print("Data stored in DuckDB (simulated Snowflake).")
