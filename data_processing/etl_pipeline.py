from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.builder.master("local[*]").appName("StockDataETL").getOrCreate()

# Load CSV data (exported from PostgreSQL or local file)
df = spark.read.csv("data/stock_data.csv", header=True, inferSchema=True)

# Data Cleaning: remove rows with null 'close' values and convert timestamp
df_clean = df.filter(col("close").isNotNull())

# Write cleaned data to a local Parquet file (simulating storage in a data warehouse)
df_clean.write.mode("overwrite").parquet("data/stock_data_cleaned.parquet")

print("ETL completed and stored locally as Parquet!")
