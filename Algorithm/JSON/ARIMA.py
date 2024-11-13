# ################################################################################################
# # SARIMA
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from datetime import datetime
# import os 

# # Load the data
# current_dir = os.getcwd()
# file_path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")

# with open(file_path, 'r') as file:
#     data = json.load(file)
    
# # Extract the quarterly net profit data
# quarters = []
# net_profit_data = []

# for quarter, values in data['Quarters'].items():
#     quarters.append(datetime.strptime(quarter, "%b '%y"))
#     net_profit_data.append(values['Profit']['Net Profit'])  # Adjusted to 'Net Profit'

# # Create a DataFrame
# df = pd.DataFrame({'Quarter': quarters, 'Net Profit': net_profit_data})
# df.set_index('Quarter', inplace=True)

# # Plot the time series with dotted lines and dots
# plt.figure(figsize=(12, 6))

# # Plot historical net profit with blue dotted line and circular markers
# plt.plot(df.index, df['Net Profit'], label='Historical Net Profit', color='blue', linestyle=':', marker='o', markersize=5)

# # Fit the SARIMA model on Net Profit data
# model = SARIMAX(df['Net Profit'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 4))
# sarima_result = model.fit()

# # Print the summary of the model
# print(sarima_result.summary())

# # Forecast the next 4 quarters (1 year)
# forecast = sarima_result.get_forecast(steps=4)
# forecast_df = forecast.summary_frame()

# # Plot the forecasted values with red dotted line and circular markers
# plt.plot(forecast_df.index, forecast_df['mean'], label='Forecast', color='red', linestyle=':', marker='o', markersize=5)

# # Fill between the confidence intervals for the forecast
# plt.fill_between(forecast_df.index,
#                  forecast_df['mean_ci_lower'],
#                  forecast_df['mean_ci_upper'], color='pink', alpha=0.3)

# # Add title and labels
# plt.title('Net Profit Forecast for Next 4 Quarters')
# plt.xlabel('Quarter')
# plt.ylabel('Net Profit (in crores)')
# plt.legend()

# # Show the plot
# plt.show()


############################### SARINA Points #############################
################################################################################################
# SARIMA
import json
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime
import os 

# Load the data
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")

with open(file_path, 'r') as file:
    data = json.load(file)
    
# Extract the quarterly net profit data
quarters = []
net_profit_data = []

for quarter, values in data['Quarters'].items():
    quarters.append(datetime.strptime(quarter, "%b '%y"))
    net_profit_data.append(values['Profit']['Net Profit'])  # Adjusted to 'Net Profit'

# Create a DataFrame
df = pd.DataFrame({'Quarter': quarters, 'Net Profit': net_profit_data})
df.set_index('Quarter', inplace=True)

# Plot the time series with dotted lines and dots
plt.figure(figsize=(15, 10))

# Plot historical net profit with blue dotted line and circular markers
plt.plot(df.index, df['Net Profit'], label='Historical Net Profit', color='blue', linestyle=':', marker='o', markersize=5)

# Annotate historical net profit values above the dots
for i, value in enumerate(df['Net Profit']):
    plt.text(df.index[i], value, f'{value:.2f}', color='blue', fontsize=7, ha='right', va='top')

# Fit the SARIMA model on Net Profit data
model = SARIMAX(df['Net Profit'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 4))
sarima_result = model.fit()

# Print the summary of the model
# print(sarima_result.summary())

# Forecast the next 4 quarters (1 year)
forecast = sarima_result.get_forecast(steps=4)
forecast_df = forecast.summary_frame()


print(forecast_df)
# exit()
# Plot the forecasted values with red dotted line and circular markers
plt.plot(forecast_df.index, forecast_df['mean'], label='Forecast', color='red', linestyle=':', marker='o', markersize=5)

# Annotate forecasted net profit values above the dots
for i, value in enumerate(forecast_df['mean']):
    if i % 2 == 0:
        var = 'top'  # Align text above the data point (even indices)
    else:
        var = 'bottom'
    plt.text(forecast_df.index[i], value, f'{value:.2f}', color='red', fontsize=7, ha='center', va=var)

# Fill between the confidence intervals for the forecast
plt.fill_between(forecast_df.index,
                 forecast_df['mean_ci_lower'],
                 forecast_df['mean_ci_upper'], color='pink', alpha=0.3)

# Add title and labels
plt.title('Net Profit Forecast for Next 4 Quarters')
plt.xlabel('Quarter')
plt.ylabel('Net Profit (in crores)')
plt.legend()

# Show the plot
plt.show()


