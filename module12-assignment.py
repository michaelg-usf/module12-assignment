# Module 12 Assignment: Business Analytics Fundamentals and Applications

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

#DATA CREATION
np.random.seed(42)

stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}
store_df = pd.DataFrame(store_data)

departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

store_performance = {"Tampa": 1.0, "Orlando": 0.85, "Miami": 1.2, "Jacksonville": 0.75, "Gainesville": 0.65}
dept_performance = {"Produce": 1.2, "Dairy": 1.0, "Bakery": 0.85, "Grocery": 0.95, "Prepared Foods": 1.1}

for date in dates:
    month = date.month
    seasonal_factor = 1.15 if month in [6,7,8] else 1.25 if month == 12 else 0.9 if month in [1,2] else 1.0
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0

    for store in stores:
        for dept in departments:
            for category in categories[dept]:
                base_sales = np.random.normal(500, 100)
                sales_amount = base_sales * store_performance[store] * dept_performance[dept] * seasonal_factor * dow_factor
                sales_amount *= np.random.normal(1.0, 0.1)

                base_margin = {"Produce":0.25,"Dairy":0.22,"Bakery":0.35,"Grocery":0.20,"Prepared Foods":0.40}[dept]
                profit_margin = np.clip(base_margin * np.random.normal(1.0,0.05), 0.15, 0.5)

                profit = sales_amount * profit_margin

                sales_data.append({
                    "Date": date, "Store": store, "Department": dept,
                    "Category": category, "Sales": round(sales_amount,2),
                    "ProfitMargin": round(profit_margin,4), "Profit": round(profit,2)
                })

sales_df = pd.DataFrame(sales_data)

# Customer data
customer_data = []
segments = ["Health Enthusiast","Gourmet Cook","Family Shopper","Budget Organic","Occasional Visitor"]

for i in range(5000):
    segment = np.random.choice(segments, p=[0.25,0.2,0.3,0.15,0.1])
    visits = np.random.randint(1,15)
    basket = np.random.uniform(40,150)
    spend = visits * basket

    tier = "Platinum" if spend>1000 else "Gold" if spend>500 else "Silver" if spend>200 else "Bronze"

    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Segment": segment,
        "VisitsPerMonth": visits,
        "AvgBasketSize": basket,
        "MonthlySpend": spend,
        "LoyaltyTier": tier
    })

customer_df = pd.DataFrame(customer_data)

# Operational data
operational_data = []
for store in stores:
    sales = sales_df[sales_df["Store"]==store]["Sales"].sum()
    profit = sales_df[sales_df["Store"]==store]["Profit"].sum()

    row = store_df[store_df["Store"]==store].iloc[0]

    operational_data.append({
        "Store": store,
        "AnnualSales": sales,
        "AnnualProfit": profit,
        "SalesPerSqFt": sales/row["SquareFootage"],
        "SalesPerStaff": sales/row["StaffCount"]
    })

operational_df = pd.DataFrame(operational_data)

# ---------------- FUNCTIONS ----------------

def analyze_sales_performance():
    df = globals().get("sales_df")
    return {
        'total_sales': df["Sales"].sum(),
        'total_profit': df["Profit"].sum(),
        'avg_profit_margin': df["ProfitMargin"].mean(),
        'sales_by_store': df.groupby("Store")["Sales"].sum(),
        'sales_by_dept': df.groupby("Department")["Sales"].sum()
    }

def visualize_sales_distribution():
    df = globals().get("sales_df")

    f1, ax1 = plt.subplots()
    df.groupby("Store")["Sales"].sum().plot(kind="bar", ax=ax1)

    f2, ax2 = plt.subplots()
    df.groupby("Department")["Sales"].sum().plot(kind="bar", ax=ax2)

    f3, ax3 = plt.subplots()
    df.groupby("Date")["Sales"].sum().plot(ax=ax3)

    return f1, f2, f3

def analyze_customer_segments():
    df = globals().get("customer_df")
    return {
        'segment_counts': df["Segment"].value_counts(),
        'segment_avg_spend': df.groupby("Segment")["MonthlySpend"].mean(),
        'segment_loyalty': pd.crosstab(df["Segment"], df["LoyaltyTier"])
    }

def analyze_sales_correlations():
    merged = pd.merge(store_df, operational_df, on="Store")
    corr = merged.corr(numeric_only=True)

    sales_corr = corr["AnnualSales"].drop("AnnualSales").sort_values(ascending=False)

    fig, ax = plt.subplots()
    sales_corr.plot(kind="bar", ax=ax)

    return {
        'store_correlations': corr,
        'top_correlations': list(zip(sales_corr.index[:5], sales_corr.values[:5])),
        'correlation_fig': fig
    }

def compare_store_performance():
    fig, ax = plt.subplots()
    operational_df.set_index("Store")["AnnualProfit"].plot(kind="bar", ax=ax)

    return {
        'efficiency_metrics': operational_df[["Store","SalesPerSqFt","SalesPerStaff"]],
        'performance_ranking': operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False),
        'comparison_fig': fig
    }

def analyze_seasonal_patterns():
    df = sales_df.copy()
    df["Month"] = df["Date"].dt.month

    monthly = df.groupby("Month")["Sales"].sum()

    fig, ax = plt.subplots()
    monthly.plot(ax=ax)

    return {
        'monthly_sales': monthly,
        'dow_sales': df.groupby(df["Date"].dt.day_name())["Sales"].sum(),
        'seasonal_fig': fig
    }

def predict_store_sales():
    from sklearn.linear_model import LinearRegression
    df = pd.merge(store_df, operational_df, on="Store")

    X = df[["SquareFootage","StaffCount","YearsOpen","WeeklyMarketingSpend"]]
    y = df["AnnualSales"]

    model = LinearRegression().fit(X,y)
    preds = pd.Series(model.predict(X), index=df["Store"])

    fig, ax = plt.subplots()
    ax.scatter(y, preds)

    return {
        'coefficients': dict(zip(X.columns, model.coef_)),
        'r_squared': model.score(X,y),
        'predictions': preds,
        'model_fig': fig
    }

def forecast_department_sales():
    df = sales_df.groupby(["Date","Department"])["Sales"].sum().unstack()
    fig, ax = plt.subplots()
    df.plot(ax=ax)

    return {
        'dept_trends': df,
        'growth_rates': df.pct_change().mean(),
        'forecast_fig': fig
    }

def identify_profit_opportunities():
    combo = sales_df.groupby(["Store","Department"])["Profit"].sum().reset_index()
    return {
        'top_combinations': combo.sort_values("Profit",ascending=False).head(10),
        'underperforming': combo.sort_values("Profit").head(10),
        'opportunity_score': combo.groupby("Store")["Profit"].sum()
    }

def develop_recommendations():
    return [
        "Invest more in high-performing stores",
        "Expand high-margin departments",
        "Target high-spending customer segments",
        "Optimize staffing levels",
        "Increase marketing in mid-tier stores"
    ]

def generate_executive_summary():
    print("GreenGrocer shows strong performance with clear opportunities for growth.")

# ---------------- MAIN ----------------

def main():
    analyze_sales_performance()
    visualize_sales_distribution()
    analyze_customer_segments()
    analyze_sales_correlations()
    compare_store_performance()
    analyze_seasonal_patterns()
    predict_store_sales()
    forecast_department_sales()
    identify_profit_opportunities()
    develop_recommendations()
    generate_executive_summary()
    plt.show()

if __name__ == "__main__":
    main()