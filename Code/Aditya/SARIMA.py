import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import sys
from statsmodels.tsa.holtwinters import ExponentialSmoothing

print("Python version:", sys.version)
print("Pandas version:", pd.__version__)

# Load and prepare data
file_path = "C:/Users/Aditya/Desktop/FyPro/Companies/Updated/Infosys_Sorted_Quarterly_Data.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Rename columns
df.rename(columns={
    "Quarterly Results of Infosys(in Rs. Cr.)": "ds",
    "Net profit/(loss) for the period": "y",
    "Total Revenue": "revenue",
    "Total Expenditure": "total_expenditure"
}, inplace=True)

# Parse dates
def parse_quarter(date_str):
    month_map = {"Mar": ("03", "31"), "Jun": ("06", "30"), "Sep": ("09", "30"), "Dec": ("12", "31")}
    parts = date_str.split()
    year = "20" + parts[1] if int(parts[1]) < 25 else "19" + parts[1]
    month, day = month_map[parts[0]]
    return pd.to_datetime(f"{year}-{month}-{day}")

df["ds"] = df["ds"].apply(parse_quarter)

# Feature engineering (for exogenous variables)
df["trend"] = np.arange(len(df))
for lag in [1, 2, 3]:
    df[f"lag_{lag}"] = df["y"].shift(lag)
df["rolling_mean"] = df["y"].rolling(window=4, min_periods=1).mean()
df["rolling_std"] = df["y"].rolling(window=4, min_periods=1).std()
df["revenue_expenditure"] = df["revenue"] * df["total_expenditure"]

# Handle missing values
df = df.ffill().bfill()

# Cap outliers
q1, q3 = np.percentile(df["y"], [25, 75])
iqr = q3 - q1
lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f"Outlier bounds: ({lower_bound:.2f}, {upper_bound:.2f})")
outliers = df["y"].apply(lambda x: x < lower_bound or x > upper_bound).sum()
print(f"Found {outliers} outliers in target variable")
df["y"] = df["y"].clip(lower_bound, upper_bound)

# Train-test split
train_size = len(df) - 10
train_df = df.iloc[:train_size].copy()
test_df = df.iloc[train_size:].copy()
dates_train, dates_test = train_df["ds"], test_df["ds"]

# Prepare exogenous variables
exog_vars = ["revenue", "total_expenditure", "revenue_expenditure"]
exog_train = train_df[exog_vars]
exog_test = test_df[exog_vars]

# SARIMA model
print("Training SARIMA model...")
# Define SARIMA parameters: (p,d,q)(P,D,Q,s)
order = (1, 1, 1)  # ARIMA component
seasonal_order = (1, 1, 1, 4)  # Seasonal component with quarterly seasonality (s=4)
sarima_model = SARIMAX(
    train_df["y"],
    exog=exog_train,
    order=order,
    seasonal_order=seasonal_order,
    enforce_stationarity=False,
    enforce_invertibility=False
).fit(disp=False)

# Predictions
train_pred = sarima_model.predict(start=0, end=len(train_df)-1, exog=exog_train)
test_pred = sarima_model.predict(
    start=len(train_df), end=len(df)-1, exog=exog_test
)

# Store predictions
train_df["sarima_pred"] = train_pred
test_df["sarima_pred"] = test_pred

# Evaluate
mae = mean_absolute_error(test_df["y"], test_df["sarima_pred"])
mse = mean_squared_error(test_df["y"], test_df["sarima_pred"])
rmse = np.sqrt(mse)
mape = np.mean(np.abs((test_df["y"] - test_df["sarima_pred"]) / test_df["y"])) * 100

print(f"Test MAE: {mae:.2f}")
print(f"Test RMSE: {rmse:.2f}")
print(f"Test MAPE: {mape:.2f}%")

# Residual plot
test_df["residual"] = test_df["y"] - test_df["sarima_pred"]
plt.figure(figsize=(8, 4))
plt.scatter(test_df["sarima_pred"], test_df["residual"], color="purple", alpha=0.7)
plt.axhline(y=0, color="black", linestyle="--")
plt.title("Residual Plot (SARIMA)")
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.grid(True)
plt.tight_layout()
plt.show()

# Forecast next 8 quarters
future = pd.DataFrame()
future["ds"] = pd.date_range(start=df["ds"].iloc[-1], periods=9, freq="QE")[1:]

# Forecast exogenous variables (revenue and expenditure)
revenue_model = ExponentialSmoothing(df["revenue"], trend="add", seasonal="add", seasonal_periods=4).fit()
expenditure_model = ExponentialSmoothing(df["total_expenditure"], trend="add", seasonal="add", seasonal_periods=4).fit()
future["revenue"] = revenue_model.forecast(8).values
future["total_expenditure"] = expenditure_model.forecast(8).values
future["revenue_expenditure"] = future["revenue"] * future["total_expenditure"]

# Prepare exogenous variables for forecasting
exog_future = future[exog_vars]

# SARIMA forecast
sarima_forecast = sarima_model.forecast(steps=8, exog=exog_future)
future["yhat"] = sarima_forecast.values

# Confidence intervals (approximate)
forecast_obj = sarima_model.get_forecast(steps=8, exog=exog_future)
conf_int = forecast_obj.conf_int(alpha=0.2)  # 80% CI
future["yhat_lower"] = conf_int.iloc[:, 0].values
future["yhat_upper"] = conf_int.iloc[:, 1].values

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(dates_train, train_df["y"], label="Training Data", color="blue")
plt.plot(dates_test, test_df["y"], label="Test Data", color="orange")
plt.plot(dates_test, test_df["sarima_pred"], label="Test Predictions", color="red", linestyle="--")
plt.plot(future["ds"], future["yhat"], label="Forecast", color="green")
plt.fill_between(future["ds"], future["yhat_lower"], future["yhat_upper"], color="green", alpha=0.2, label="Forecast 80% CI")
plt.axvline(x=df["ds"].iloc[-1], color="black", linestyle="--", label="Forecast Start")
plt.title("SARIMA Net Profit Forecast")
plt.xlabel("Date")
plt.ylabel("Net Profit (Rs. Cr.)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print forecast
print("\nForecast for next 8 quarters:")
print(future[["ds", "yhat"]].round(2).to_string(index=False))