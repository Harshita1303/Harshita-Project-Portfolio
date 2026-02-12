# 🏦 Credit Card Default Risk Prediction

This project predicts whether a customer will default in the next month using six months of historical repayment behavior.

It is designed as a **cost-sensitive, imbalanced classification system**, where reducing financial risk (False Negatives) is more important than maximizing raw accuracy.

---

# 📌 Project Description

Financial institutions face significant risk when customers fail to repay credit obligations. The goal of this project is to build a machine learning model that predicts the probability of default in the next billing cycle using historical financial and repayment data.

Unlike traditional models that optimize only accuracy, this project emphasizes:

- Risk-aware modeling  
- Class imbalance handling  
- Threshold optimization  
- Financial impact alignment  

The final output is a **probability-based risk scoring model** suitable for real-world financial decision-making.

---
# 🛠 Tech Stack & Tools Used

## 💻 Programming Language
- Python

## 📚 Libraries 
- Pandas
- NumPy
- Matplotlib
- Scikit-Learn
- Joblib
- Streamlit
- MLflow
---

## 📊 Dataset Overview

Total Variables: 25  

#### Customer Information
- ID
- SEX
- AGE
- EDUCATION
- MARRIAGE

#### Credit Information
- LIMIT_BAL

#### Repayment Status (6 Months)
- PAY_0 to PAY_6

#### Billing Amounts
- BILL_AMT1 to BILL_AMT6

#### Payment Amounts
- PAY_AMT1 to PAY_AMT6

#### Target
- default.payment.next.month (1 = Default, 0 = No Default)

---

## 🧹 Data Cleaning & Preprocessing

- Removed duplicates
- Dropped ID column
- Fixed undocumented categories:
  - EDUCATION (0,5,6 → 4)
  - MARRIAGE (0 → 3)
- Converted mixed datatype columns to numeric
- Cleaned special characters from financial columns
- Median imputation for missing values
- Stratified train-test split
- MinMax feature scaling

---

## 📈 Exploratory Data Analysis (EDA)

### 🔹 Class Distribution
- ~78% Non-Defaulters  
- ~22% Defaulters  

⚠️ Dataset is imbalanced.

---

### 🔹 Key Insights from EDA

- Repeated repayment delays strongly correlate with default.
- Lower education levels show slightly higher default probability.
- Men exhibit slightly higher default rates than women.
- Lower credit limits are associated with higher default risk.
- Married men show higher risk in demographic interaction analysis.

Repayment behavior (`PAY_0`–`PAY_6`) emerged as the strongest predictive feature group.
---

### 🧠 Feature Engineering

Created interaction feature: SE_MA = Combination of SEX and MARRIAGE

This captured demographic behavioral patterns such as:

- Married men → Higher default probability  
- Single women → Lower default probability  

---

## ⚙️ Model Development

### Train-Test Strategy
Used **Stratified Train-Test Split** to preserve class distribution.

### Feature Scaling
Applied **MinMaxScaler** for normalized feature scaling.

---

### Models Implemented

- Logistic Regression 
- Decision Tree 
- Random Forest 
- XGBoost 
---

## 🎯 Threshold Optimization (Core Contribution)

Default threshold = `0.5` ❌  

Used probability outputs (`predict_proba()`) and tested: 0.5 → 0.4 → 0.3 → 0.2

Optimal threshold selected:0.30

This resulted in:

- Reduced False Negatives
- Improved Recall
- Improved F1 Score
- Better financial risk alignment  

---

## 📉 Evaluation Metrics

- Precision  
- Recall  
- F1 Score  
- Confusion Matrix  
- Precision–Recall Curve  

Accuracy was not used as the primary metric due to imbalance.

---

## 🧪 MLflow Experiment Tracking
Configured local MLflow tracking:

```python
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Credit_Default_Risk")
```

Tracked:

- Model type
- Hyperparameters
- Threshold
- Accuracy
- Recall
- F1 Score

Run locally at:

```
http://localhost:5000
```
---


## 🚀 Streamlit Deployment

The model is deployed using Streamlit.
The app allows users to:

- Enter customer financial details
- View input summary
- Generate probability of default
- Classify into:
  - Low Risk
  - Medium Risk
  - High Risk

Risk Logic:

```python
proba = model.predict_proba(input_df)[0, 1]

if proba < 0.30:
    Low Risk
elif proba < 0.50:
    Medium Risk
else:
    High Risk
```

The deployed app transforms the ML model into a real-time financial risk scoring tool.

---

## 📊 Dashboard Visualization

The project also includes a Tableau dashboard that visualizes:

- Default distribution
- Risk category distribution
- Credit utilization trends
- Revenue at risk
- Age group risk analysis
- Payment delay vs default rate

This bridges ML output with business interpretation.

---

## 💾 Model Persistence

The final trained model was saved using:

```python
joblib.dump(rf_model, "credit_default_rf_balanced.joblib")
```

This ensures:

- Reproducibility  
- Easy deployment  
- Model version control  
- Production readiness  

The saved model can be directly loaded in a deployment environment for real-time risk scoring.

---

## 🏆 Results & Insights

### 📊 Final Model Selected: Random Forest

Random Forest was selected because of:

* Strong minority-class detection  
* Stability across different data splits  
* Ability to handle nonlinear feature interactions  
* Balanced precision–recall tradeoff  
* Robust performance on structured financial data  

---

### 📈 Performance Improvements via Threshold Tuning

Default classification threshold (`0.5`) was suboptimal for financial risk modeling.
After testing multiple thresholds, the optimal value selected was: 0.30

#### Impact at Threshold 0.30:

- Recall improved significantly  
- False Negatives reduced  
- F1 Score increased  
- Model better aligned with financial objectives  

This adjustment directly reduced the risk of missing high-risk customers.

---

## 💼 Business Insights Generated

- Customers with repeated payment delays are much more likely to default.
- A growing difference between billed amount and payment amount shows increasing financial stress.
- Customers with lower credit limits tend to have higher default risk.
- The model helps identify risky customers early so banks can take preventive action.
- Lowering the prediction threshold to 0.30 reduced missed defaulters and helped protect financial losses.

This project demonstrates how technical model optimization translates directly into improved financial risk management.

---
