import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# Step 1: Prepare the data
data = {
    "Quarter": ["Sep '13", "Dec '13", "Mar '14", "Jun '14", "Sep '14", "Dec '14", "Mar '15", "Jun '15", "Sep '15"],
    "Total Income": [16607.72, 16692.65, 16893.91, 17000.50, 17200.30, 17350.20, 17400.00, 17500.60, 17600.00],
    "Employee Costs": [5428.79, 5430.93, 5354.04, 5500.00, 5600.10, 5700.25, 5800.50, 5900.60, 6000.00],
    "Depreciation": [261.74, 280.36, 297.21, 310.40, 320.50, 330.60, 340.80, 350.90, 360.00],
    "Other Expenses": [5430.48, 5482.53, 5974.83, 6000.10, 6100.00, 6200.25, 6300.50, 6400.60, 6500.00],
    "Net Profit": [5486.71, 5498.83, 5267.83, 5100.00, 5200.30, 5300.40, 5400.50, 5500.60, 5600.00]
}

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Step 2: Prepare the features and target
X = df[["Total Income", "Employee Costs", "Depreciation", "Other Expenses"]]  # Independent variables
y = df["Net Profit"]  # Dependent variable (target)

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Make predictions
y_pred = model.predict(X_test)

# Step 6: Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# Output the evaluation metrics
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
print(f"Mean Absolute Error: {mae}")

# Step 7: Visualize Actual vs Predicted Net Profit
plt.scatter(y_test, y_pred)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel("Actual Net Profit")
plt.ylabel("Predicted Net Profit")
plt.title("Actual vs Predicted Net Profit")
plt.show()

# Step 8: Making Future Predictions (example with new data)
new_data = {
    "Total Income": [55000.0],  # Example future value
    "Employee Costs": [25000.0],
    "Depreciation": [1000.0],
    "Other Expenses": [12000.0]
}
new_data_df = pd.DataFrame(new_data)

# Predict Net Profit for the new data
future_profit = model.predict(new_data_df)
print(f"Predicted Net Profit for the new quarter: {future_profit[0]}")
