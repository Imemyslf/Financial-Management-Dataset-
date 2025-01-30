import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Initialize model and data variables
model = None
df = None
X_train = X_test = y_train = y_test = None

# Load JSON and train model
def load_json():
    global model, df, X_train, X_test, y_train, y_test

    # Ask user to select the JSON file
    file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )

    if not file_path:
        return

    # Load JSON data
    try:
        with open(file_path) as f:
            data = json.load(f)

        quarters = data["Quarters"]
        records = []

        for quarter, values in quarters.items():
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

        df = pd.DataFrame(records)

        # Select input features and target
        X = df[['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses']]
        y = df['Net Profit']

        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_test, _, y_test, _ = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        messagebox.showinfo("Info", "Model trained successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON file.\n{e}")

# Display training data
def show_training_data():
    if df is not None:
        train_data = pd.concat([X_train, y_train], axis=1)
        display_data(train_data, "Training Data")
    else:
        messagebox.showwarning("Warning", "Please load data and train the model first.")

# Display testing data
def show_testing_data():
    if df is not None:
        test_data = pd.concat([X_test, y_test], axis=1)
        display_data(test_data, "Testing Data")
    else:
        messagebox.showwarning("Warning", "Please load data and train the model first.")

# Display data in a new window
def display_data(data, title):
    data_window = tk.Toplevel(root)
    data_window.title(title)
    text = tk.Text(data_window, wrap="none")
    text.insert(tk.END, data.to_string())
    text.pack()

# Manual prediction input
def predict_manual_input():
    if model is None:
        messagebox.showwarning("Warning", "Please load data and train the model first.")
        return

    try:
        # Get user inputs
        total_income = float(entry_income.get())
        employees_cost = float(entry_cost.get())
        depreciation = float(entry_depreciation.get())
        other_expenses = float(entry_expenses.get())

        # Create a DataFrame for manual input
        manual_input = pd.DataFrame([[total_income, employees_cost, depreciation, other_expenses]],
                                    columns=['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses'])

        # Predict net profit for the manual input
        manual_pred = model.predict(manual_input)
        result_label.config(text=f"Predicted Net Profit: {manual_pred[0]:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Initialize the main window
root = tk.Tk()
root.title("Financial Analysis GUI")
root.geometry("500x300")

# Create frame for loading JSON and model training
frame_load = tk.Frame(root)
frame_load.pack(pady=10)

load_button = tk.Button(frame_load, text="Load JSON and Train Model", command=load_json)
load_button.pack()

# Frame for displaying training/testing data
frame_display = tk.Frame(root)
frame_display.pack(pady=10)

train_data_button = tk.Button(frame_display, text="Show Training Data", command=show_training_data)
train_data_button.grid(row=0, column=0, padx=5)

test_data_button = tk.Button(frame_display, text="Show Testing Data", command=show_testing_data)
test_data_button.grid(row=0, column=1, padx=5)

# Frame for manual input and prediction
frame_manual = tk.Frame(root)
frame_manual.pack(pady=10)

tk.Label(frame_manual, text="Total Income From Operations:").grid(row=0, column=0, padx=5, sticky="e")
entry_income = tk.Entry(frame_manual)
entry_income.grid(row=0, column=1, padx=5)

tk.Label(frame_manual, text="Employees Cost:").grid(row=1, column=0, padx=5, sticky="e")
entry_cost = tk.Entry(frame_manual)
entry_cost.grid(row=1, column=1, padx=5)

tk.Label(frame_manual, text="Depreciation:").grid(row=2, column=0, padx=5, sticky="e")
entry_depreciation = tk.Entry(frame_manual)
entry_depreciation.grid(row=2, column=1, padx=5)

tk.Label(frame_manual, text="Other Expenses:").grid(row=3, column=0, padx=5, sticky="e")
entry_expenses = tk.Entry(frame_manual)
entry_expenses.grid(row=3, column=1, padx=5)

predict_button = tk.Button(frame_manual, text="Predict Net Profit", command=predict_manual_input)
predict_button.grid(row=4, column=0, columnspan=2, pady=10)

# Label to display prediction result
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Run the GUI
root.mainloop()
