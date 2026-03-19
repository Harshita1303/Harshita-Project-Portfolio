from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lead
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import GBTClassifier

# Create Spark session with Hive support

spark = SparkSession.builder \
    .appName("Customer_Churn_GBT_For_PowerBI") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Load Gold table from Hive

df = spark.table("churn_project.gold_user_monthly")

# Create churn label
# If user does not appear next month → churn = 1
# Otherwise → churn = 0

window_spec = Window.partitionBy("userId") \
                    .orderBy("event_year", "event_month")

df = df.withColumn(
    "next_month",
    lead("event_month").over(window_spec)
)

df = df.withColumn(
    "churn",
    col("next_month").isNull().cast("integer")
).drop("next_month")

# Prepare feature vector

feature_columns = [
    "total_plays",
    "total_listening_time",
    "total_sessions"
]

assembler = VectorAssembler(
    inputCols=feature_columns,
    outputCol="features"
)

df = assembler.transform(df)

# Split data into training and testing

train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

# Train Gradient Boosted Trees model

gbt = GBTClassifier(
    featuresCol="features",
    labelCol="churn",
    maxIter=30,
    maxDepth=5
)

model = gbt.fit(train_df)

# Generate predictions

predictions = model.transform(test_df)


# Save predictions as CSV for Power BI

predictions.select(
    "userId",
    "event_year",
    "event_month",
    "total_plays",
    "total_listening_time",
    "total_sessions",
    "churn",
    "prediction"
).write.mode("overwrite") \
 .option("header", True) \
 .csv("/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/data/powerbi_predictions")

print("Churn predictions saved for Power BI.")