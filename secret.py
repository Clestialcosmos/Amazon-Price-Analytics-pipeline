import pandas as pd
import glob
import os
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

#______conn connector___________#
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tanishq07@"
)

#_________conn establish__________#
def setup_database(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS amazon_pipeline")
    conn.database = "amazon_pipeline"

#_________pre-requisite____________#
filelist = glob.glob("*.csv")
excludedfile = "asin_dataset_1000.csv"
filteredfile = [
    f for f in filelist if os.path.basename(f) != excludedfile
]
print(filteredfile)

#_________Extract___________#
def extract(filepath):
    try:
        df = pd.read_csv(filepath)
        df["source_file"] = os.path.basename(filepath)
        print("File read successfully")
    except Exception as e:
        print(e)
        return None
    return df

#___________TRANSFORM___________#
def transform(df):
    try:
        df.columns = df.columns.str.strip().str.lower()
        if "price" not in df.columns:
            print("Price column missing skipping gold layer")
            return df

        df["price"] = df["price"].astype(str).str.replace("₹", "").str.replace(",", "")
        df["price"] = pd.to_numeric(df["price"], errors='coerce')
        df = df.dropna(subset=["price"])
        df = df[df["price"] > 0]

        if "product" in df.columns:
            df = df.drop_duplicates(subset=["product"])

        df["ingestion_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Data Transformed")
        return df
    except Exception as e:
        print(f"Error arises as {e}")
        return None

#__________GOLD LAYER__________#
def goldlayer(df):
    try:
        import random
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA

        df["current_price"] = df["price"].apply(lambda x: x * random.uniform(0.7, 1.1))  #0.7 (−30%) and 1.1 (+10%)
        df["min_price"] = df["price"]
        df["price_change"] = ((df["current_price"] - df["min_price"]) / df["min_price"])

        features = df[['min_price', 'current_price', 'price_change']].fillna(0)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(features)  #will do mean = 0  and variance = 1 for unbiased in PCA

        pca = PCA(n_components=1)
        df["pca_score"] = pca.fit_transform(X_scaled)

        threshold = df['pca_score'].std() * 2
        df['pca_anomaly'] = abs(df['pca_score']) > threshold
        df = df[df['pca_anomaly'] == False]

        df["discount"] = df["min_price"] - df["current_price"]
        df["discount_percent"] = (df["discount"] / df["min_price"]) * 100

        print("Gold Layer executed")
        return df

    except Exception as e:
        print("Gold layer error", e)
        return df

#___________LOAD________#
def load(tn, df, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {tn} (
            product TEXT,
            price FLOAT,
            current_price FLOAT,
            min_price FLOAT,
            discount FLOAT,
            discount_percent FLOAT,
            source_file TEXT,
            ingestion_time DATETIME
        )
        """)

        for _, row in df.iterrows():
            cursor.execute(f"""
                INSERT INTO {tn}
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                row.get('product'),
                row.get('price'),
                row.get('current_price'),
                row.get('min_price'),
                row.get('discount'),
                row.get('discount_percent'),
                row.get('source_file'),
                row.get('ingestion_time')
            ))

        conn.commit()
        print("Data loaded successfully")

    except Exception as e:
        print("Error arise during loading", e)

#_____________VISUALIZE_____________#
def visualize(df):

    print("Price Distribution histogram loading ............")
    plt.figure()
    plt.hist(df["price"], bins=50)
    plt.title("Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()
    print("Histogram succefully loaded .............")

    print("DISCOUNT ANALYSIS SCATTER PLOT GRAPH is Loading............")
    plt.figure()
    plt.scatter(df["min_price"], df["discount_percent"])
    plt.title("Discount vs Price")
    plt.xlabel("Min Price")
    plt.ylabel("Discount %")
    plt.grid(True)
    plt.show()
    print("Scatter plot for discount_analysis is loaded successfully................")

    print("SCATTER plot for PCA Visualisation is loading............")
    plt.figure()
    plt.scatter(df["pca_score"], df["price_change"])
    plt.title("PCA Score vs Price Change")
    plt.xlabel("PCA Score")
    plt.ylabel("Price Change")
    plt.grid(True)
    plt.show()
    print("PCA VISUALISATION SHOWED SUCCESSFULLY..............")

    print("ALL CSV FILE ANALYSIS ........... BAR + PIE LOADING................")

    data = df.groupby("source_file")["price"].mean().sort_values()

    # BAR CHART
    plt.figure()
    data.plot(kind="bar")
    plt.title("Avg Price per File")
    plt.xlabel("Source File")
    plt.ylabel("Average Price")
    plt.grid(True)
    plt.show()

    # PIE CHART
    plt.figure()
    plt.pie(data, labels=data.index, autopct='%1.1f%%')
    plt.title("Price Contribution per File")
    plt.show()

    print("LOADED SUCCESSFULL..................................")

#_______START__________#
if __name__ == "__main__":
    setup_database(conn)
    a = os.getcwd()

    all_data = []

    for i in filteredfile:
        df = extract(os.path.join(a, i))
        if df is None:
            continue

        df = transform(df)
        if df is None:
            continue

        df = goldlayer(df)
        if df is None or df.empty:
            print("No valid data to load")
            continue

        all_data.append(df)

        load("filtered_table", df, conn)


    final_df = pd.concat(all_data, ignore_index=True)
    visualize(final_df)