# 🛒 Amazon Price Analytics Pipeline

## 📌 Overview

This project is an end-to-end **ETL (Extract, Transform, Load) pipeline** built using Python.
It processes multiple Amazon product datasets, performs data cleaning, applies feature engineering, detects anomalies using PCA, and generates insightful visualizations.

---

## 🚀 Features

* 📥 Multi-file CSV ingestion
* 🧹 Data cleaning & preprocessing
* 🧠 Feature engineering (price change, discount %)
* 📊 PCA-based anomaly detection
* 📈 Data visualization using Matplotlib
* 🗄️ MySQL database integration
* 🔁 Modular pipeline architecture

---

## 🏗️ Pipeline Architecture

```text
Extract → Transform → Gold Layer → Load → Visualize
```

### 🔹 1. Extract

* Reads multiple CSV files
* Adds source tracking (`source_file`)

### 🔹 2. Transform

* Cleans price column (₹, commas)
* Handles missing & invalid values
* Removes duplicates
* Adds ingestion timestamp

### 🔹 3. Gold Layer (Feature Engineering)

* Creates:

  * `current_price`
  * `price_change`
  * `discount`
  * `discount_percent`
* Applies PCA for dimensionality reduction
* Detects and removes anomalies

### 🔹 4. Load

* Stores processed data into MySQL
* Creates table if not exists

### 🔹 5. Visualization

* 📊 Price distribution (Histogram)
* 📉 Discount vs Price (Scatter)
* 🧠 PCA Visualization
* 📊 Avg price per file (Bar chart)
* 🥧 Price contribution (Pie chart)

---

## 🧠 PCA Logic (Simplified)

PCA reduces multiple features into a single score:

* Input: `min_price, current_price, price_change`
* Output: `pca_score`

Outliers are detected using:

```
threshold = 2 * standard deviation
```

Data points beyond this threshold are removed.

---

## 🛠️ Tech Stack

* Python 🐍
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* MySQL

---

## 📂 Project Structure

```
amazon_pipeline/
│
├── data/                  # Input CSV files
├── Perfect_deals.csv     # Output deals file
├── pipeline.py           # Main pipeline script
├── README.md
```

---

## ⚙️ How to Run

### 1. Install dependencies

```
pip install pandas numpy matplotlib scikit-learn mysql-connector-python
```

### 2. Run the pipeline

```
python pipeline.py
```

---

## 📊 Sample Outputs

* Cleaned dataset in MySQL
* Perfect deals CSV
* Visual graphs:

  * Histogram
  * Scatter plots
  * Bar & Pie charts

---

## 🎯 Key Learnings

* Building modular ETL pipelines
* Data preprocessing techniques
* Feature engineering strategies
* PCA for dimensionality reduction
* Data visualization best practices

---

## 🚀 Future Improvements

* Replace PCA with Isolation Forest for anomaly detection
* Add Airflow for pipeline scheduling
* Use bulk inserts for faster DB loading
* Build dashboard using Streamlit

---

## 👨‍💻 Author

Tanishq Tomar

---
