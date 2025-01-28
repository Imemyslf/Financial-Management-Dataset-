import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Example DataFrame (replace with your actual data)
data = {
    'date': pd.date_range(start='2020-01-01', periods=100, freq='D'),
    'profit': [50 + i + (i % 10) * 2 for i in range(100)]  # Example profit data
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Rename columns to fit Prophet's input requirements
df = df.rename(columns={'date': 'ds', 'profit': 'y'})

# Initialize and fit the Prophet model
model = Prophet(daily_seasonality=True)  # You can adjust the seasonality settings
model.fit(df)

# Make future predictions (periods=30 means 30 days ahead)
future = model.make_future_dataframe(periods=30)  # Correct usage of periods argument
forecast = model.predict(future)

# Plot the forecast
model.plot(forecast)
plt.title('Profit Prediction using Prophet')
plt.xlabel('Date')
plt.ylabel('Profit')
plt.show()

# Plot components (trend, seasonality)
model.plot_components(forecast)
plt.show()
