from pyspark.sql import SparkSession
from pyspark.sql.functions import count, sum, countDistinct

spark = SparkSession.builder \
    .appName("Gold_With_Hive") \
    .master("local[*]") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read Silver
silver_df = spark.read.parquet(
    "/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/data/silver"
)

# Aggregate
gold_df = silver_df.groupBy(
    "userId",
    "event_year",
    "event_month",
    "level"
).agg(
    count("*").alias("total_plays"),
    sum("length").alias("total_listening_time"),
    countDistinct("sessionId").alias("total_sessions")
)

# Create DB
spark.sql("CREATE DATABASE IF NOT EXISTS churn_project")

# Save as Hive table
gold_df.write \
    .mode("overwrite") \
    .partitionBy("event_year", "event_month") \
    .saveAsTable("churn_project.gold_user_monthly")

print("Gold table successfully written to Hive")