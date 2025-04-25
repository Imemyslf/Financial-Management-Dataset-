import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
import matplotlib.pyplot as plt
import sys

print("Python version:", sys.version)
print("XGBoost version:", xgb.__version__)
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

# Feature engineering
df["trend"] = np.arange(len(df))
for lag in [1, 2, 3]:
    df[f"lag_{lag}"] = df["y"].shift(lag)
df["rolling_mean"] = df["y"].rolling(window=4, min_periods=1).mean()
df["rolling_std"] = df["y"].rolling(window=4, min_periods=1).std()
df["revenue_expenditure"] = df["revenue"] * df["total_expenditure"]

# Handle missing values
df = df.ffill().bfill()  # Updated to use ffill()/bfill() instead of fillna(method=)

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

# Prophet model
print("Training models...")
prophet_df = train_df[["ds", "y"]].copy()
prophet_df["revenue"] = train_df["revenue"]
prophet_df["total_expenditure"] = train_df["total_expenditure"]

prophet_model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    seasonality_mode="additive"
)
prophet_model.add_regressor("revenue")
prophet_model.add_regressor("total_expenditure")
prophet_model.fit(prophet_df)

# Prophet predictions
prophet_train_pred = prophet_model.predict(prophet_df)
train_df["prophet_pred"] = prophet_train_pred["yhat"].values

prophet_test_df = test_df[["ds", "revenue", "total_expenditure"]].copy()
prophet_test_pred = prophet_model.predict(prophet_test_df)
test_df["prophet_pred"] = prophet_test_pred["yhat"].values

# Compute residuals
train_df["residual"] = train_df["y"] - train_df["prophet_pred"]
test_df["residual"] = test_df["y"] - test_df["prophet_pred"]

# Features for XGBoost
features = ["trend", "lag_1", "lag_2", "lag_3", "rolling_mean", "revenue", "total_expenditure", "revenue_expenditure"]
X_train = train_df[features]
y_train_residual = train_df["residual"].replace([np.inf, -np.inf], np.nan).fillna(0)
X_test = test_df[features]
y_test_residual = test_df["residual"].replace([np.inf, -np.inf], np.nan).fillna(0)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_train_scaled = pd.DataFrame(X_train_scaled, columns=features, index=X_train.index)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=features, index=X_test.index)

# XGBoost model
params = {
    "objective": "reg:squarederror",
    "max_depth": 3,
    "learning_rate": 0.2,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "eval_metric": "mae",
    "random_state": 42
}
xgb_model = xgb.XGBRegressor(**params)
xgb_model.fit(X_train_scaled, y_train_residual)

# Predict residuals
xgb_train_residual_pred = xgb_model.predict(X_train_scaled)
xgb_test_residual_pred = xgb_model.predict(X_test_scaled)

# Final predictions
train_df["final_pred"] = train_df["prophet_pred"] + xgb_train_residual_pred
test_df["final_pred"] = test_df["prophet_pred"] + xgb_test_residual_pred

# Ensure no NaN values in predictions
test_df["final_pred"] = test_df["final_pred"].fillna(test_df["prophet_pred"])

# Evaluate
# Evaluate
from sklearn.metrics import mean_squared_error, r2_score

mae = mean_absolute_error(test_df["y"], test_df["final_pred"])
mse = mean_squared_error(test_df["y"], test_df["final_pred"])
rmse = np.sqrt(mse)
r2 = r2_score(test_df["y"], test_df["final_pred"])
mape = np.mean(np.abs((test_df["y"] - test_df["final_pred"]) / test_df["y"])) * 100

print(f"Test MAE: {mae:.2f}")
print(f"Test RMSE: {rmse:.2f}")
# print(f"Test R² Score: {r2:.4f}")
print(f"Test MAPE: {mape:.2f}%")

# Residual plot
plt.figure(figsize=(8, 4))
plt.scatter(test_df["final_pred"], test_df["residual"], color="purple", alpha=0.7)
plt.axhline(y=0, color='black', linestyle='--')
plt.title("Residual Plot")
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.grid(True)
plt.tight_layout()
plt.show()


# Forecast next 8 quarters
future = pd.DataFrame()
future["ds"] = pd.date_range(start=df["ds"].iloc[-1], periods=9, freq="QE")[1:]

# Forecast revenue and expenditure
revenue_model = ExponentialSmoothing(df["revenue"], trend="add", seasonal="add", seasonal_periods=4).fit()
expenditure_model = ExponentialSmoothing(df["total_expenditure"], trend="add", seasonal="add", seasonal_periods=4).fit()
future["revenue"] = revenue_model.forecast(8).values
future["total_expenditure"] = expenditure_model.forecast(8).values

prophet_future_pred = prophet_model.predict(future)
future["prophet_pred"] = prophet_future_pred["yhat"].values
future["yhat_lower"] = prophet_future_pred["yhat_lower"].values
future["yhat_upper"] = prophet_future_pred["yhat_upper"].values

# Prepare future features
future["trend"] = np.arange(len(df), len(df) + 8)
for lag in [1, 2, 3]:
    future[f"lag_{lag}"] = np.nan

# Initialize with last known values
future.loc[future.index[0], "lag_1"] = df["y"].iloc[-1]
future.loc[future.index[0], "lag_2"] = df["y"].iloc[-2]
future.loc[future.index[0], "lag_3"] = df["y"].iloc[-3]

future["rolling_mean"] = df["y"].rolling(window=4).mean().iloc[-1]
future["revenue_expenditure"] = future["revenue"] * future["total_expenditure"]

# Fill any remaining NAs
future = future.ffill().bfill()

# Scale future features
future_scaled = scaler.transform(future[features])
future_scaled = pd.DataFrame(future_scaled, columns=features, index=future.index)

# Make predictions iteratively
predictions = []
for i in range(8):
    row = future_scaled.iloc[i:i+1].copy()
    residual_pred = xgb_model.predict(row)[0]
    pred = future["prophet_pred"].iloc[i] + residual_pred
    predictions.append(pred)
    
    # Update lags for next prediction if not last iteration
    if i < 7:
        future_scaled.iloc[i+1, future_scaled.columns.get_loc("lag_1")] = pred
        future_scaled.iloc[i+1, future_scaled.columns.get_loc("lag_2")] = future_scaled.iloc[i, future_scaled.columns.get_loc("lag_1")]
        future_scaled.iloc[i+1, future_scaled.columns.get_loc("lag_3")] = future_scaled.iloc[i, future_scaled.columns.get_loc("lag_2")]

future["yhat"] = predictions

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(dates_train, train_df["y"], label="Training Data", color="blue")
plt.plot(dates_test, test_df["y"], label="Test Data", color="orange")
plt.plot(dates_test, test_df["final_pred"], label="Test Predictions", color="red", linestyle="--")
plt.plot(future["ds"], future["yhat"], label="Forecast", color="green")
plt.fill_between(future["ds"], future["yhat_lower"], future["yhat_upper"], color="green", alpha=0.2, label="Forecast 80% CI")
plt.axvline(x=df["ds"].iloc[-1], color="black", linestyle="--", label="Forecast Start")
plt.title("Hybrid Prophet + XGBoost Net Profit Forecast")
plt.xlabel("Date")
plt.ylabel("Net Profit (Rs. Cr.)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Feature importance
xgb.plot_importance(xgb_model, importance_type="gain")
plt.title("XGBoost Feature Importance (Residuals)")
plt.tight_layout()
plt.show()

# Print forecast
print("\nForecast for next 8 quarters:")
print(future[["ds", "yhat"]].round(2).to_string(index=False))