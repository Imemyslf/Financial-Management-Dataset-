import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.metrics import mean_squared_error, r2_score
import os
import pydotplus
from IPython.display import Image
from io import StringIO
import graphviz

# Define the file path
current_dir = os.getcwd()
path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")

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

# Initialize and train the decision tree regressor
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model on the test set
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error (Test): {mse}')
print(f'R^2 Score (Test): {r2}')

# Optional: Display actual vs predicted values for the test set
result_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print("\nTest Set - Actual vs Predicted:")
print(result_df)

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

# Call the manual input function
predict_manual_input()

# Visualize the decision tree
dot_data = StringIO()
export_graphviz(model, out_file=dot_data, 
                filled=True, rounded=True,
                feature_names=X.columns,
                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())
