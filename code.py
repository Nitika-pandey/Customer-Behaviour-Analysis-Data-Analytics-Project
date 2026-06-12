import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files

sns.set_style("whitegrid")

print("📂 Upload CSV file")
uploaded = files.upload()

file_name = list(uploaded.keys())[0]
df = pd.read_csv(file_name)
df.columns = df.columns.str.strip()

print(f"\n📊 DATA LOADED | Rows: {len(df)} | Columns: {len(df.columns)}")
print("⚠ Using first 2000 rows for analysis")

if len(df) > 2000:
    df = df.head(2000)

numeric_cols = df.select_dtypes(include="number").columns.tolist()

ignore = [
    "Loan_Account_No", "Debit_Card_No", "Credit_Card_No",
    "Demat_Account_No", "Current_Account_No", "Savings_Account_No"
]

numeric_cols = [c for c in numeric_cols if c not in ignore]

if len(numeric_cols) == 0:
    raise SystemExit("No valid numeric business columns found")

target = "Total_Spend" if "Total_Spend" in df.columns else numeric_cols[0]

df["Segment"] = pd.qcut(df[target], 3, labels=["Low", "Medium", "High"])

print("\n" + "="*50)
print("👥 CUSTOMER SEGMENTATION")
print("="*50)
print(df["Segment"].value_counts())

print("\n" + "="*50)
print("📊 BUSINESS KPI DASHBOARD")
print("="*50)

for col in numeric_cols:
    print(f"• {col}: {df[col].mean():.2f}")

print("\n" + "="*50)
print("🧠 BEHAVIOURAL INSIGHTS")
print("="*50)

insights = []

if "Total_Spend" in df.columns:
    high = (df["Total_Spend"] > df["Total_Spend"].quantile(0.8)).mean() * 100
    insights.append(f"{high:.1f}% users are high-value customers")

if "Logins" in df.columns:
    low_eng = (df["Logins"] < df["Logins"].median()).mean() * 100
    insights.append(f"{low_eng:.1f}% users show low engagement risk")

if "Transactions" in df.columns:
    insights.append(f"Average transactions per user: {df['Transactions'].mean():.1f}")

if "Complaints" in df.columns:
    complaint_rate = df["Complaints"].mean() * 100
    if complaint_rate > 5:
        insights.append(f"Complaint rate: {complaint_rate:.2f}% (needs monitoring)")
    else:
        insights.append(f"Complaint rate: {complaint_rate:.2f}% (under control)")

if "Logins" in df.columns and "Total_Spend" in df.columns:
    corr = df["Logins"].corr(df["Total_Spend"])
    if corr > 0.5:
        insights.append("Strong relationship: engagement drives revenue")
    elif corr > 0:
        insights.append("Moderate relationship between engagement and revenue")
    else:
        insights.append("Weak relationship between engagement and revenue")

for i, ins in enumerate(insights, 1):
    print(f"{i}. {ins}")

print("\n" + "="*50)
print("📊 GRAPH GENERATOR")
print("="*50)

print("\nAvailable columns:")
for i, col in enumerate(numeric_cols, 1):
    print(f"{i} - {col}")

idx = int(input("\nSelect column number: ")) - 1
x = numeric_cols[idx]

print("\nSelect graph type:")
print("1 - Histogram")
print("2 - Box Plot")

g = input("Choice: ").strip()

print("\nSelect color:")
print("1 - Blue")
print("2 - Green")
print("3 - Red")
print("4 - Purple")
print("5 - Orange")

color_map = {
    "1": "blue",
    "2": "green",
    "3": "red",
    "4": "purple",
    "5": "orange"
}

color = color_map.get(input("Choice: "), "blue")

print("\nSelect size:")
print("1 - Small")
print("2 - Medium")
print("3 - Large")

size_map = {
    "1": (6, 4),
    "2": (8, 5),
    "3": (12, 7)
}

figsize = size_map.get(input("Choice: "), (8, 5))

plt.figure(figsize=figsize)

if g == "1":
    sns.histplot(df[x], kde=True, color=color)
elif g == "2":
    sns.boxplot(y=df[x], color=color)
else:
    sns.histplot(df[x], kde=True, color=color)

plt.tight_layout()
plt.show()

print("\n✅ Analysis Complete")
