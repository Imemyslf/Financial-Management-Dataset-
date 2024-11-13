import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf   


# Load the data from the JSON file
with open('Infosys Ltd_total_revenue.json', 'r') as f:
    data = json.load(f)

# Extract the net profit data and create a DataFrame
df = pd.DataFrame(data['Total Profit for each quarter'].values(), index=data['Total Profit for each quarter'].keys(), columns=['Net Profit'])
df.index = pd.to_datetime(df.index)

# Visualize the time series data
plt.figure(figsize=(12, 6))
plt.plot(df['Net Profit'])
plt.xlabel('Date')
plt.ylabel('Net Profit')
plt.title('Net Profit Time Series')
plt.show()

# Check for stationarity
from statsmodels.tsa.stattools import adfuller
result = adfuller(df['Net Profit'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:', result[4])

# If the p-value is greater than 0.05, the series is not stationary
if result[1] > 0.05:
    df['Net Profit'] = df['Net Profit'].diff().dropna()

# Plot ACF and PACF to determine p and q
plot_acf(df['Net Profit'], lags=20)
plot_pacf(df['Net Profit'], lags=20)
plt.show()

# Based on ACF and PACF plots, determine p, d, and q
p = 2  # Adjust p based on ACF plot
d = 1  # Adjust d based on stationarity check
q = 1  # Adjust q based on PACF plot

# Create and fit the ARIMA model
model = ARIMA(df['Net Profit'], order=(p, d, q))
model_fit = model.fit()

# Make predictions
forecast, se, conf_int = model_fit.forecast(steps=4)  # Forecast the next 4 quarters

# Print the forecast
print('Forecast:', forecast)

# Visualize the forecast
plt.figure(figsize=(12, 6))
plt.plot(df['Net Profit'], label='Actual')
plt.plot(forecast, label='Forecast')
plt.xlabel('Date')
plt.ylabel('Net Profit')
plt.title('Actual vs. Forecast')
plt.legend()
plt.show()