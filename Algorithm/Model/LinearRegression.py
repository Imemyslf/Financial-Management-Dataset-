import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os
import matplotlib.pyplot as plt

# Define the file path
current_dir = os.getcwd()
path = os.path.join(current_dir,"Main_Data","MoneyControl", "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")

print(path)

# Load JSON data
with open(path) as f:
    data = json.load(f)

# Convert JSON to a DataFrame by extracting data for each quarter
quarters = data["Quarters"]
records = []

for quarter, values in quarters.items():
    # Flatten each quarter's data and add the 'Quarter' as a column
    record = {
        'Quarter': quarter,
        'Total Income From Operations': values['Income']['Total Income From Operations'],
        'Employees Cost': values['Expenditure']['Employees Cost'],
        'Depreciation': values['Expenditure']['depreciat'],
        'Other Expenses': values['Expenditure']['Other Expenses'],
        'Total Income sum': values['Profit']['Total Income sum'],
        'Total Expenditure sum': values['Profit']['Total Expenditure_sum'],
        'Net Profit': values['Profit']['Net Profit']
    }
    records.append(record)

# Create DataFrame from records
df = pd.DataFrame(records)

# Select input features and target
X = df[['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses']]
y = df['Net Profit']


# Split data: 60% training, 20% testing, 20% manual testing
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_test, X_manual_test, y_test, y_manual_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Add the 'Quarter' column to the training and testing data for display
X_train['Quarter'] = df.loc[X_train.index, 'Quarter']
X_test['Quarter'] = df.loc[X_test.index, 'Quarter']

# Display the training data with quarter names
print("Training Data:")
print(pd.concat([X_train[['Quarter']], X_train.drop('Quarter', axis=1), y_train], axis=1))
training_data = pd.concat([X_train[['Quarter']], X_train.drop('Quarter', axis=1), y_train], axis=1)
# training_data.to_excel("Training_Data.xlsx", index=False)

# print("\nTraining data saved to 'Training_Data.xlsx'")

# Display the testing data with quarter names
print("\nTesting Data:")
print(pd.concat([X_test[['Quarter']], X_test.drop('Quarter', axis=1), y_test], axis=1))
# testing_data = pd.concat([X_test[['Quarter']], X_test.drop('Quarter', axis=1), y_test], axis=1)
# testing_data.to_excel("Testing_data.xlsx",index=False)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train.drop('Quarter', axis=1), y_train)

# Make predictions on the test set
y_pred = model.predict(X_test.drop('Quarter', axis=1))

# Evaluate the model on the test set
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error (Test): {mse}')
print(f'R^2 Score (Test): {r2}')

# Optional: Display actual vs predicted values for the test set
result_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print("\nTest Set - Actual vs Predicted:")
print(result_df)

# Find remaining quarters that were not used in the training or testing sets
used_quarters = X_train['Quarter'].tolist() + X_test['Quarter'].tolist()
remaining_quarters = [quarter for quarter in df['Quarter'] if quarter not in used_quarters]

# Print remaining quarters
print("\nRemaining Quarters (Not Used in Training or Testing):")
print(remaining_quarters)

print("Intercept (β0):", model.intercept_)
print("Coefficients (β1, β2, β3, β4):", model.coef_)

# Plot actual vs. predicted Net Profit for training data
y_train_pred = model.predict(X_train.drop('Quarter', axis=1))

plt.figure(figsize=(10, 6))
plt.plot(y_train.values, label="Actual Net Profit", marker='o')
plt.plot(y_train_pred, label="Predicted Net Profit", marker='x')

plt.xlabel("Training Data Points")
plt.ylabel("Net Profit")
plt.title("Actual vs. Predicted Net Profit on Training Data")
plt.legend()
plt.grid(True)
plt.show()

# Function for manual testing
def predict_manual_input():
    print("\n--- Manual Input Prediction ---")
    # Prompt user for manual inputs
    total_income = float(input("Enter Total Income From Operations: "))
    employees_cost = float(input("Enter Employees Cost: "))
    depreciation = float(input("Enter Depreciation: "))
    other_expenses = float(input("Enter Other Expenses: "))

    # Create a DataFrame for the manual input
    manual_input = pd.DataFrame([[total_income, employees_cost, depreciation, other_expenses]],
                                columns=['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses'])

    # Predict net profit for the manual input
    manual_pred = model.predict(manual_input)
    print(f"Predicted Net Profit: {manual_pred[0]}")

# Choice loop for manual predictions
choice = True
while(choice):
    user_choice = input("\n\n Predict Quarterly Net Profit Choice: Press (Y?N):- ")
    if user_choice.lower() == "y" or user_choice.lower() == "yes":
        predict_manual_input()
    else:
        choice = False