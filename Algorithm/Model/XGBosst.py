import json
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import os

current_dir = os.getcwd()
path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")

print(path)
# Load JSON data
with open(path) as f:
    data = json.load(f)

# Parse data into a DataFrame
quarters = data["Quarters"]
df = pd.DataFrame({
    'Total Income From Operations': [quarters[q]["Income"]["Total Income From Operations"] for q in quarters],
    'Employees Cost': [quarters[q]["Expenditure"]["Employees Cost"] for q in quarters],
    'Depreciation': [quarters[q]["Expenditure"]["depreciat"] for q in quarters],
    'Other Expenses': [quarters[q]["Expenditure"]["Other Expenses"] for q in quarters],
    'Net Profit': [quarters[q]["Profit"]["Net Profit"] for q in quarters]
})

# Define features and target variable
X = df.drop(columns=["Net Profit"])
y = df["Net Profit"]

# Split data: 60% train, 20% test, 20% unused
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_test, X_unused, y_test, y_unused = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Train the model
model = XGBRegressor()
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error on test data: {mse}")

# Display the unused data
print("Unused data:")
print(X_unused)
print(y_unused)
