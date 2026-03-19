from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import (from_json, col, lower, trim, to_timestamp, year, month)

# Create Spark Session

spark = SparkSession.builder \
    .appName("BronzeToSilverStreaming") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Bronze Schema (Required for readStream)

bronze_schema = StructType([
    StructField("json_data", StringType(), True)
])

# Actual Event JSON Schema

json_schema = StructType([
    StructField("status", IntegerType(), True),
    StructField("gender", StringType(), True),
    StructField("length", DoubleType(), True),
    StructField("firstName", StringType(), True),
    StructField("lastName", StringType(), True),
    StructField("level", StringType(), True),
    StructField("userId", StringType(), True),
    StructField("sessionId", IntegerType(), True),
    StructField("location", StringType(), True),
    StructField("page", StringType(), True),
    StructField("song", StringType(), True),
    StructField("artist", StringType(), True),
    StructField("ts", LongType(), True)
])

# Read Bronze as Streaming Source

bronze_df = spark.readStream \
    .schema(bronze_schema) \
    .format("parquet") \
    .load("/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/data/bronze")

# Parse JSON

parsed_df = bronze_df.select(
    from_json(col("json_data"), json_schema).alias("data")
).select("data.*")

# Cleaning & Validation Logic

silver_df = parsed_df \
    .filter(col("userId").isNotNull()) \
    .filter(trim(col("userId")) != "") \
    .filter(col("page") == "NextSong") \
    .filter(col("length").isNotNull()) \
    .filter(col("length") > 0)

# Normalize subscription level

silver_df = silver_df.withColumn(
    "level",
    lower(trim(col("level")))
)

# Convert Epoch → Timestamp 

silver_df = silver_df.withColumn(
    "event_time",
    to_timestamp((col("ts") / 1000).cast("timestamp"))
)

# Remove records where timestamp failed

silver_df = silver_df.filter(col("event_time").isNotNull())

# Deduplication with Watermark 

silver_df = silver_df \
    .withWatermark("event_time", "10 minutes") \
    .dropDuplicates(["userId", "sessionId", "ts"])

# Add Partition Columns

silver_df = silver_df \
    .withColumn("event_year", year("event_time")) \
    .withColumn("event_month", month("event_time"))

# Write Silver Layer

query = silver_df.writeStream \
    .format("parquet") \
    .option("path", "/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/data/silver") \
    .option("checkpointLocation", "/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/checkpoints/silver") \
    .partitionBy("event_year", "event_month") \
    .outputMode("append") \
    .start()

print("Bronze to Silver Streaming Started...")

query.awaitTermination()