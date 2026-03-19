# 🎧 Customer Churn Prediction System

An end-to-end **real-time churn prediction pipeline** built using streaming data, big data technologies, and machine learning to proactively identify users likely to churn.

---

## 🚀 Problem Statement
User activity data (song plays, sessions) was available only as raw logs and not structured for analytics.  
This made it impossible to predict churn in advance, leading to **reactive decision-making**.

👉 This project solves that by building a **scalable pipeline** that:
- Processes real-time logs
- Converts them into structured features
- Predicts user churn proactively

---


---

## 🛠️ Tech Stack

| Layer          | Technology |
|---------------|-----------|
| Streaming     | Apache Kafka |
| Processing    | Apache Spark (Structured Streaming + Batch) |
| Storage       | Parquet |
| Warehouse     | Apache Hive |
| ML Model      | XGBoost |
| Visualization | Tableau |
| Orchestration | Apache Airflow |
| Language      | Python |

---

## ⚙️ Key Components

### 🔹 Data Ingestion (Kafka)
- Distributed, partitioned log system  
- Handles high-volume streaming data  
- Ensures durability and replay capability  

---

### 🔹 Processing (Spark)
- Micro-batch streaming engine  
- Converts raw logs → structured data  
- Implements Bronze → Silver → Gold architecture  

---

### 🔹 Data Layers
- **Bronze:** Raw streaming data (Parquet)  
- **Silver:** Clean, structured, deduplicated data  
- **Gold:** Aggregated user-level features  

---

### 🔹 Machine Learning
- Model: **XGBoost**
- Features:
  - Total plays
  - Listening time
  - Session count
- Handles **non-linear patterns & class imbalance**
- Evaluated using **F1-score, Recall**

---

### 🔹 Churn Definition
- Based on **user inactivity in next month**
- Implemented using **window functions (LEAD)**

---

### 🔹 Visualization (Tableau)
- Churn rate trends  
- Engagement vs churn  
- Risk segmentation  
- Model performance (confusion matrix)  

---

### 🔹 Orchestration (Airflow)
- Automates pipeline:
  - Bronze → Silver → Gold → ML  
- Handles scheduling, retries, dependencies  

---

## 📊 Business Impact

- 📉 Reduced reactive churn handling  
- 🎯 Identified high-risk users proactively  
- 📈 Improved retention strategy insights  
- 🧠 Enabled data-driven decision making  

---

## 💡 Key Highlights

- Real-time streaming pipeline  
- Scalable big data architecture  
- End-to-end ML lifecycle  
- Production-ready orchestration  
- Business-focused dashboard insights  

---

## 🎤 Interview Summary

> Built an end-to-end streaming pipeline using Kafka and Spark, transformed raw logs into structured features across Bronze-Silver-Gold layers, trained a churn prediction model using XGBoost/GBT, and automated the workflow using Airflow with insights delivered via Tableau dashboards.

---


