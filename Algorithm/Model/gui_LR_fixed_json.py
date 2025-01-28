import customtkinter
from customtkinter import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import json
import os

# Load JSON data and prepare the DataFrame
current_dir = os.getcwd()
path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")

with open(path) as f:
    data = json.load(f)

# Extract and organize data for each quarter
quarters = data["Quarters"]
records = []

for quarter, values in quarters.items():
    record = {
        'Quarter': quarter,
        'Total Income From Operations': values['Income']['Total Income From Operations'],
        'Employees Cost': values['Expenditure']['Employees Cost'],
        'Depreciation': values['Expenditure']['depreciat'],
        'Other Expenses': values['Expenditure']['Other Expenses'],
        'Net Profit': values['Profit']['Net Profit']
    }
    records.append(record)

df = pd.DataFrame(records)

# Define input features and target variable
X = df[['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses']]
y = df['Net Profit']

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# GUI Setup with customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Initialize main app window
app = CTk()
app.title("Linear Regression Predictor")
app.geometry("500x400")
app.resizable(False, False)

# Define function for making predictions on manual inputs
def predict_manual():
    try:
        # Fetch user inputs
        total_income = float(entry_income.get())
        employees_cost = float(entry_employees.get())
        depreciation = float(entry_depreciation.get())
        other_expenses = float(entry_expenses.get())
        
        # Create a DataFrame for the manual input 
        manual_input = pd.DataFrame([[total_income, employees_cost, depreciation, other_expenses]],
                                    columns=['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses'])
        
        # Predict net profit for the manual input
        manual_pred = model.predict(manual_input)
        result_label.configure(text=f"Predicted Net Profit: {manual_pred[0]:.2f}", fg_color="green")
    except Exception as e:
        result_label.configure(text="Invalid input. Please enter valid numbers.", fg_color="red")

# Function to display model performance
def display_model_performance():
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    performance_label.configure(text=f"Model Performance:\nMSE: {mse:.2f}\nR^2 Score: {r2:.2f}")

# Title label for the application
title_label = CTkLabel(app, text="Quarterly Net Profit Predictor", font=("Arial", 20, "bold"), text_color="lightblue")
title_label.pack(pady=10)

# Input fields for user data
entry_income = CTkEntry(app, placeholder_text="Total Income From Operations", width=400, font=("Arial", 14), fg_color="gray20", text_color="white")
entry_income.pack(pady=5)

entry_employees = CTkEntry(app, placeholder_text="Employees Cost", width=400, font=("Arial", 14), fg_color="gray20", text_color="white")
entry_employees.pack(pady=5)

entry_depreciation = CTkEntry(app, placeholder_text="Depreciation", width=400, font=("Arial", 14), fg_color="gray20", text_color="white")
entry_depreciation.pack(pady=5)

entry_expenses = CTkEntry(app, placeholder_text="Other Expenses", width=400, font=("Arial", 14), fg_color="gray20", text_color="white")
entry_expenses.pack(pady=5)

# Predict button for manual inputs
predict_button = CTkButton(app, text="Predict Net Profit", command=predict_manual, width=200, font=("Arial", 14, "bold"), fg_color="blue", hover_color="darkblue")
predict_button.pack(pady=10)

# Result label to display prediction results
result_label = CTkLabel(app, text="", width=400, height=25, fg_color="grey", corner_radius=12)
result_label.pack(pady=10)

# Performance button to display model metrics
performance_button = CTkButton(app, text="Show Model Performance", command=display_model_performance, width=200, font=("Arial", 14, "bold"), fg_color="blue", hover_color="darkblue")
performance_button.pack(pady=10)

# Label to display model performance
performance_label = CTkLabel(app, text="", width=400, height=50, fg_color="grey", corner_radius=12)
performance_label.pack(pady=10)

# Run the app main loop
app.mainloop()
