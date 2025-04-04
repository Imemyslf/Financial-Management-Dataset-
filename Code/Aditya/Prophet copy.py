# from prophet import Prophet
# import pandas as pd
# import matplotlib.pyplot as plt

# # Load and prepare data
# file_path = "C:/Users/Aditya/Desktop/FyPro/Companies/Updated/TCS_Sorted_Quarterly_Data.xlsx"
# df = pd.read_excel(file_path, sheet_name="Sheet1")

# # Rename columns
# df.rename(columns={
#     "Quarterly Results of Tata Consultancy Services(in Rs. Cr.)": "ds",
#     "Net profit/(loss) for the period": "y",
#     "Total Revenue": "revenue",
#     "Total Expenditure": "total_expenditure"
# }, inplace=True)

# # Parse dates
# def parse_quarter(date_str):
#     month_map = {"Mar": ("03", "31"), "Jun": ("06", "30"), "Sep": ("09", "30"), "Dec": ("12", "31")}
#     parts = date_str.split()
#     year = "20" + parts[1] if int(parts[1]) < 25 else "19" + parts[1]
#     month, day = month_map[parts[0]]
#     return pd.to_datetime(f"{year}-{month}-{day}")

# df["ds"] = df["ds"].apply(parse_quarter)

# # Train-test split
# train_size = len(df) - 10
# train_df = df.iloc[:train_size].copy()
# test_df = df.iloc[train_size:].copy()

# # Prepare data for Prophet
# prophet_df = train_df[["ds", "y"]].copy()
# prophet_df["revenue"] = train_df["revenue"]
# prophet_df["total_expenditure"] = train_df["total_expenditure"]

# # Initialize and configure Prophet model
# prophet_model = Prophet(
#     yearly_seasonality=True,       # Capture yearly patterns
#     weekly_seasonality=False,      # No weekly data
#     daily_seasonality=False,       # No daily data
#     seasonality_mode="additive",  
#     changepoint_prior_scale=0.5,   # Allows moderate flexibility in trend changes
#     interval_width=0.8             # 80% confidence interval
# )

# # Add external regressors
# prophet_model.add_regressor("revenue")
# prophet_model.add_regressor("total_expenditure")

# # Fit the model
# prophet_model.fit(prophet_df)

# # Make predictions on training data
# prophet_train_pred = prophet_model.predict(prophet_df)

# # Make predictions on test data
# prophet_test_df = test_df[["ds", "revenue", "total_expenditure"]].copy()
# prophet_test_pred = prophet_model.predict(prophet_test_df)

# # Plot the components
# fig_components = prophet_model.plot_components(prophet_train_pred)
# plt.suptitle("Prophet Model Components", y=1.02)
# plt.tight_layout()
# plt.show()

# # Plot the forecast
# fig_forecast = prophet_model.plot(prophet_train_pred)
# plt.plot(test_df["ds"], test_df["y"], color="orange", label="Actual Test Data")
# plt.title("Prophet Forecast vs Actuals")
# plt.legend()
# plt.tight_layout()
# plt.show()

# # Evaluate performance
# from sklearn.metrics import mean_absolute_error

# train_mae = mean_absolute_error(train_df["y"], prophet_train_pred["yhat"])
# test_mae = mean_absolute_error(test_df["y"], prophet_test_pred["yhat"])

# print(f"Training MAE: {train_mae:.2f}")
# print(f"Test MAE: {test_mae:.2f}")

# # Create future dataframe for forecasting
# future = prophet_model.make_future_dataframe(periods=8, freq="Q")
# future["revenue"] = df["revenue"].mean()  # In practice, you'd forecast these
# future["total_expenditure"] = df["total_expenditure"].mean()

# # Make forecast
# forecast = prophet_model.predict(future)

# # Plot the final forecast
# fig = prophet_model.plot(forecast)
# plt.title("3i Infotech Net Profit Forecast with Prophet")
# plt.xlabel("Date")
# plt.ylabel("Net Profit (Rs. Cr.)")
# plt.tight_layout()
# plt.show()


from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Load and prepare data
file_path = "C:/Users/Aditya/Desktop/FyPro/Companies/Updated/TCS_Sorted_Quarterly_Data.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Rename columns
df.rename(columns={
    "Quarterly Results of Tata Consultancy Services(in Rs. Cr.)": "ds",
    "Net profit/(loss) for the period": "y",
    "Total Revenue": "revenue",
    "Total Expenditure": "total_expenditure"
}, inplace=True)

# Convert quarterly strings to datetime format
def parse_quarter(date_str):
    month_map = {"Mar": ("03", "31"), "Jun": ("06", "30"), "Sep": ("09", "30"), "Dec": ("12", "31")}
    parts = date_str.split()
    year = "20" + parts[1] if int(parts[1]) < 25 else "19" + parts[1]
    month, day = month_map[parts[0]]
    return pd.to_datetime(f"{year}-{month}-{day}")

df["ds"] = df["ds"].apply(parse_quarter)

# Train-test split
train_size = len(df) - 10
train_df = df.iloc[:train_size].copy()
test_df = df.iloc[train_size:].copy()

# Prepare data for Prophet
prophet_df = train_df[["ds", "y"]].copy()
prophet_df["revenue"] = train_df["revenue"]
prophet_df["total_expenditure"] = train_df["total_expenditure"]

# Initialize Prophet model
prophet_model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=False,  
    daily_seasonality=False,  
    seasonality_mode="multiplicative",  
    changepoint_prior_scale=2.0,  
    interval_width=0.8  
)

# Add custom seasonality
prophet_model.add_seasonality(name="yearly", period=365.25, fourier_order=10)
prophet_model.add_seasonality(name="quarterly", period=91.25, fourier_order=8)

# Add regressors
prophet_model.add_regressor("revenue")
prophet_model.add_regressor("total_expenditure")

# Fit the model
prophet_model.fit(prophet_df)

# Make predictions
prophet_train_pred = prophet_model.predict(prophet_df)
prophet_test_df = test_df[["ds", "revenue", "total_expenditure"]].copy()
prophet_test_pred = prophet_model.predict(prophet_test_df)

# Plot trend, yearly, and quarterly components
fig_components = prophet_model.plot_components(prophet_train_pred)
plt.suptitle("Prophet Model Components (Trend, Yearly, Quarterly)", y=1.02)
plt.tight_layout()
plt.show()

# Plot forecast vs actual data
fig_forecast = prophet_model.plot(prophet_train_pred)
plt.plot(test_df["ds"], test_df["y"], color="orange", label="Actual Test Data")
plt.title("Prophet Forecast vs Actuals (Yearly & Quarterly Seasonality)")
plt.legend()
plt.tight_layout()
plt.show()

# Evaluate performance
train_mae = mean_absolute_error(train_df["y"], prophet_train_pred["yhat"])
test_mae = mean_absolute_error(test_df["y"], prophet_test_pred["yhat"])
train_rmse = np.sqrt(mean_squared_error(train_df["y"], prophet_train_pred["yhat"]))
test_rmse = np.sqrt(mean_squared_error(test_df["y"], prophet_test_pred["yhat"]))

print(f"Training MAE: {train_mae:.2f}")
print(f"Test MAE: {test_mae:.2f}")
print(f"Training RMSE: {train_rmse:.2f}")
print(f"Test RMSE: {test_rmse:.2f}")

# Future forecasting
future = prophet_model.make_future_dataframe(periods=8, freq="QE")  # Updated freq from Q to QE
future["revenue"] = df["revenue"].rolling(4, min_periods=1).mean()
future["total_expenditure"] = df["total_expenditure"].rolling(4, min_periods=1).mean()

forecast = prophet_model.predict(future)

# Final forecast plot
fig = prophet_model.plot(forecast)
plt.title("TCS Net Profit Forecast with Prophet (Yearly & Quarterly)")
plt.xlabel("Date")
plt.ylabel("Net Profit (Rs. Cr.)")
plt.tight_layout()
plt.show()
