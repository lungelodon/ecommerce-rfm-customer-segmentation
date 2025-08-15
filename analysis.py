import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_excel("/home/ubuntu/data_portfolio/E_commerce_RFM_Customer_Segmentation/Online Retail.xlsx")

# Data Cleaning and Preprocessing
df.dropna(subset=["CustomerID"], inplace=True)
df = df[df["Quantity"] > 0]
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# RFM Analysis
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda date: (snapshot_date - date.max()).days, # Recency
    "InvoiceNo": lambda num: num.nunique(),                       # Frequency
    "TotalPrice": lambda price: price.sum()                       # Monetary
})

rfm.rename(columns={
    "InvoiceDate": "Recency",
    "InvoiceNo": "Frequency",
    "TotalPrice": "Monetary"
}, inplace=True)

# Assign RFM scores using custom quantile functions
rfm["R_Score"] = rfm["Recency"].rank(pct=True).apply(lambda x: 5 if x <= 0.2 else (4 if x <= 0.4 else (3 if x <= 0.6 else (2 if x <= 0.8 else 1))))
rfm["F_Score"] = rfm["Frequency"].rank(pct=True).apply(lambda x: 1 if x <= 0.2 else (2 if x <= 0.4 else (3 if x <= 0.6 else (4 if x <= 0.8 else 5))))
rfm["M_Score"] = rfm["Monetary"].rank(pct=True).apply(lambda x: 1 if x <= 0.2 else (2 if x <= 0.4 else (3 if x <= 0.6 else (4 if x <= 0.8 else 5))))

# Convert scores to integer type
rfm["R_Score"] = rfm["R_Score"].astype(int)
rfm["F_Score"] = rfm["F_Score"].astype(int)
rfm["M_Score"] = rfm["M_Score"].astype(int)

# Combine RFM scores to create an RFM segment
rfm["RFM_Segment"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

# Define customer segments based on RFM scores
def rfm_level(df):
    if df["RFM_Segment"] == "555":
        return "Champions"
    elif df["RFM_Segment"] == "544":
        return "Loyal Customers"
    elif df["RFM_Segment"] == "455":
        return "Potential Loyalists"
    elif df["RFM_Segment"] == "355":
        return "New Customers"
    elif df["RFM_Segment"] == "111":
        return "Lost Customers"
    else:
        return "Others"

rfm["Customer_Segment"] = rfm.apply(rfm_level, axis=1)

print("\nRFM DataFrame with Segments Head:")
print(rfm.head())

# Visualize customer segments
segment_counts = rfm["Customer_Segment"].value_counts().sort_index()
plt.figure(figsize=(10, 7))
sns.barplot(x=segment_counts.index, y=segment_counts.values, palette="viridis")
plt.title("Customer Segmentation by RFM")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.savefig("/home/ubuntu/data_portfolio/E_commerce_RFM_Customer_Segmentation/customer_segments.png")
print("Customer segments plot saved as customer_segments.png")

# Save RFM results to CSV
rfm.to_csv("/home/ubuntu/data_portfolio/E_commerce_RFM_Customer_Segmentation/rfm_results.csv")

print("\nAnalysis complete. RFM results saved to CSV and plot generated.")


