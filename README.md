<h1 align="center">🛒 Amazon Price Analytics Pipeline</h1>

<p align="center">
  <b>End-to-End ETL Pipeline for Amazon Product Data</b><br>
  <i>Data Cleaning • PCA • Anomaly Detection • Visualization • MySQL</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Pandas-Data-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/MySQL-Database-green?style=for-the-badge">
</p>

---

## 📌 Overview

This project builds a complete **data engineering + analytics pipeline** that:

* Ingests multiple Amazon datasets
* Cleans and transforms pricing data
* Applies **PCA for anomaly detection**
* Stores results in **MySQL**
* Generates visual insights using **Matplotlib**

---

## 🚀 Features

### 📥 Data Ingestion

* Multi-file CSV processing
* Automatic `source_file` tracking

### 🧹 Data Cleaning

* Removes ₹ symbol & commas
* Handles missing values
* Removes duplicates

### 🧠 Feature Engineering

* `price_change`
* `discount`
* `discount_percent`

### 📊 Anomaly Detection

* PCA-based dimensionality reduction
* Outlier filtering using standard deviation

### 📈 Visualization

* Histogram (price distribution)
* Scatter plots
* Bar chart
* Pie chart

### 🗄️ Database Integration

* MySQL table creation
* Data loading pipeline

---

## 🏗️ Pipeline Architecture

```text
Extract → Transform → Gold Layer → Load → Visualize
```

---

## 🧠 PCA Logic

```python
features = ['min_price', 'current_price', 'price_change']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

pca = PCA(n_components=1)
df['pca_score'] = pca.fit_transform(X_scaled)

threshold = 2 * df['pca_score'].std()
df = df[df['pca_score'].abs() <= threshold]
```

---

## 📊 Visual Output

* 📉 Price Distribution
* 📊 Discount Analysis
* 🧠 PCA Scatter Plot
* 📊 Avg Price per File
* 🥧 Price Contribution (Pie Chart)

---

## 🛠️ Tech Stack

| Category      | Tools         |
| ------------- | ------------- |
| Language      | Python 🐍     |
| Data          | Pandas, NumPy |
| ML            | Scikit-learn  |
| Visualization | Matplotlib    |
| Database      | MySQL         |

---

## 📂 Project Structure

```
amazon_pipeline/
│
├── data/
├── Perfect_deals.csv
├── pipeline.py
└── README.md
```

---

## ⚙️ How to Run

```bash
pip install pandas numpy matplotlib scikit-learn mysql-connector-python
python pipeline.py
```

---

## 🚀 Future Improvements

* 🌲 Isolation Forest for better anomaly detection
* ⏰ Airflow scheduling
* ⚡ Bulk database inserts
* 📱 Streamlit dashboard

---

## 👨‍💻 Author

**Tanishq Tomar**

---

<p align="center">
  ⭐ If you like this project, give it a star!
</p>
