from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("KafkaToBronze") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "music_events") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# Convert binary value to string
bronze_df = df.selectExpr("CAST(value AS STRING) AS json_data")

# Write to Bronze
query = bronze_df.writeStream \
    .format("parquet") \
    .option("path", "/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/data/bronze") \
    .option("checkpointLocation", "/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/checkpoints/bronze") \
    .outputMode("append") \
    .start()

print("Bronze Streaming Started...")

query.awaitTermination()