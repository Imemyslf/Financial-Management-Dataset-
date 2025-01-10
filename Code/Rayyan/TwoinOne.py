import json
import pandas as pd
import os
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the data
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "Main_Data", "MoneyControl", "Companies", 
                         "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")

with open(file_path, 'r') as file:
    data = json.load(file)

# Extract data for SARIMA forecasting
quarters = []
params = {
    'Total Income From Operations': [],
    'Employees Cost': [],
    'Depreciation': [],
    'Other Expenses': []
}

for quarter, values in data['Quarters'].items():
    quarters.append(datetime.strptime(quarter, "%b '%y"))
    params['Total Income From Operations'].append(values['Income']['Total Income From Operations'])
    params['Employees Cost'].append(values['Expenditure']['Employees Cost'])
    params['Depreciation'].append(values['Expenditure']['depreciat'])
    params['Other Expenses'].append(values['Expenditure']['Other Expenses'])

# SARIMA Forecasting
forecasted_values = {}
for param_name, param_data in params.items():
    df = pd.DataFrame({'Quarter': quarters, param_name: param_data})
    df.set_index('Quarter', inplace=True)

    # Fit the SARIMA model
    model = SARIMAX(df[param_name], order=(1, 1, 1), seasonal_order=(1, 1, 1, 4))
    result = model.fit()

    # Forecast the next 4 quarters
    forecast = result.get_forecast(steps=4)
    forecast_df = forecast.summary_frame()
    forecast_df.index = pd.date_range(start=df.index[-1] + pd.offsets.QuarterEnd(), periods=4, freq='Q')

    # Store the forecasted mean values
    forecasted_values[param_name] = forecast_df['mean'].tolist()

# Extract net profit and related parameters from JSON
records = []
net_profit_data = []
for quarter, values in data['Quarters'].items():
    record = {
        'Quarter': quarter,
        'Total Income From Operations': values['Income']['Total Income From Operations'],
        'Employees Cost': values['Expenditure']['Employees Cost'],
        'Depreciation': values['Expenditure']['depreciat'],
        'Other Expenses': values['Expenditure']['Other Expenses'],
        'Net Profit': values['Profit']['Net Profit']
    }
    records.append(record)
    net_profit_data.append(values['Profit']['Net Profit'])

# Create a DataFrame
df = pd.DataFrame(records)

# Prepare training and testing data for MLR
X = df[['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses']]
y = df['Net Profit']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train MLR model
mlr_model = LinearRegression()
mlr_model.fit(X_train, y_train)

# Evaluate MLR model
y_pred = mlr_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MLR Model Evaluation:\nMSE: {mse}\nR²: {r2}")

# Predict net profit for forecasted quarters
forecast_quarters = pd.DataFrame(forecasted_values)
forecast_quarters.columns = ['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses']

net_profit_predictions_mlr = mlr_model.predict(forecast_quarters)

# Forecast net profits using SARIMA
df_net_profit = pd.DataFrame({'Quarter': quarters, 'Net Profit': net_profit_data})
df_net_profit.set_index('Quarter', inplace=True)

sarima_model = SARIMAX(df_net_profit['Net Profit'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 4))
sarima_result = sarima_model.fit()

sarima_forecast = sarima_result.get_forecast(steps=4)
sarima_forecast_df = sarima_forecast.summary_frame()
sarima_forecast_df.index = pd.date_range(start=df_net_profit.index[-1] + pd.offsets.QuarterEnd(), periods=4, freq='Q')

# Add SARIMA forecasts to the DataFrame
forecast_quarters['Net Profit (SARIMA)'] = sarima_forecast_df['mean'].values
forecast_quarters['Net Profit (MLR)'] = net_profit_predictions_mlr
forecast_quarters.index = ['Q1', 'Q2', 'Q3', 'Q4']

print("\nForecasted Net Profits for Next 4 Quarters:")
print(forecast_quarters)

# Plot Forecasted Net Profits
plt.figure(figsize=(12, 6))
plt.plot(forecast_quarters.index, forecast_quarters['Net Profit (SARIMA)'], label="SARIMA Forecast", marker='o', color='blue')
plt.plot(forecast_quarters.index, forecast_quarters['Net Profit (MLR)'], label="MLR Prediction", marker='x', color='red')

plt.xlabel("Quarters")
plt.ylabel("Net Profit")
plt.title("Comparison of SARIMA and MLR Forecasts for Net Profit")
plt.legend()
plt.grid(True)
plt.show()
