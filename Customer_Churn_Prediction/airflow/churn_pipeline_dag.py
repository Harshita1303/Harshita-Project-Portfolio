from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "harshita",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="churn_end_to_end_pipeline",
    default_args=default_args,
    description="Kafka → Bronze → Silver → Gold → Hive → ML Pipeline",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Bronze Layer
    bronze_task = BashOperator(
        task_id="bronze_layer",
        bash_command="""
        spark-submit /home/sunbeam/Desktop/Project/Customer_Churn_Prediction/spark/spark_bronze.py
        """
    )

    # Silver Layer
    silver_task = BashOperator(
        task_id="silver_layer",
        bash_command="""
        spark-submit /home/sunbeam/Desktop/Project/Customer_Churn_Prediction/spark/spark_silver.py
        """
    )

    # Gold Layer
    gold_task = BashOperator(
        task_id="gold_layer",
        bash_command="""
        spark-submit /home/sunbeam/Desktop/Project/Customer_Churn_Prediction/spark/spark_gold.py
        """
    )

    # ML Job
    ml_task = BashOperator(
        task_id="ml_training",
        bash_command="""
        spark-submit /home/sunbeam/Desktop/Project/Customer_Churn_Prediction/spark/spark_ml.py
        """
    )

    # Define task order
    bronze_task >> silver_task >> gold_task >> ml_task