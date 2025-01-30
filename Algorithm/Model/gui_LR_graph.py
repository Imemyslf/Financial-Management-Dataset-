import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os
import customtkinter
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load and preprocess data
current_dir = os.getcwd()
path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")
with open(path) as f:
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
        'Net Profit': values['Profit']['Net Profit']
    }
    records.append(record)

df = pd.DataFrame(records)
X = df[['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses']]
y = df['Net Profit']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# GUI setup
app = CTk()
app.title("Financial Model - Net Profit Prediction")
app.geometry("800x600")

# Display MSE and R2
label_mse = CTkLabel(app, text=f"Mean Squared Error: {mse:.2f}", font=("Arial", 14))
label_mse.pack(pady=10)
label_r2 = CTkLabel(app, text=f"R^2 Score: {r2:.2f}", font=("Arial", 14))
label_r2.pack(pady=10)

# Function to predict manually
def predict_manual_input():
    total_income = float(entry_income.get())
    employees_cost = float(entry_employees.get())
    depreciation = float(entry_depreciation.get())
    other_expenses = float(entry_other.get())
    
    manual_input = pd.DataFrame([[total_income, employees_cost, depreciation, other_expenses]],
                                columns=['Total Income From Operations', 'Employees Cost', 'Depreciation', 'Other Expenses'])
    manual_pred = model.predict(manual_input)
    label_result.configure(text=f"Predicted Net Profit: {manual_pred[0]:.2f}")

# Manual input fields
CTkLabel(app, text="Enter Total Income From Operations:").pack()
entry_income = CTkEntry(app)
entry_income.pack(pady=5)

CTkLabel(app, text="Enter Employees Cost:").pack()
entry_employees = CTkEntry(app)
entry_employees.pack(pady=5)

CTkLabel(app, text="Enter Depreciation:").pack()
entry_depreciation = CTkEntry(app)
entry_depreciation.pack(pady=5)

CTkLabel(app, text="Enter Other Expenses:").pack()
entry_other = CTkEntry(app)
entry_other.pack(pady=5)

# Predict button for manual input
btn_predict = CTkButton(app, text="Predict Net Profit", command=predict_manual_input)
btn_predict.pack(pady=5)

# Result label for manual prediction
label_result = CTkLabel(app, text="", font=("Arial", 14, "bold"))
label_result.pack(pady=5)

# Plotting function
def plot_graph():
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(y_test.values, label="Actual Net Profit", color="blue", marker="o")
    ax.plot(y_pred, label="Predicted Net Profit", color="red", marker="x")
    ax.legend(loc="upper left")
    ax.set_title("Actual vs Predicted Net Profit")
    ax.set_xlabel("Test Set Quarter")
    ax.set_ylabel("Net Profit")

    # Display figure in GUI
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

# Plot graph button
btn_plot = CTkButton(app, text="Show Graph", command=plot_graph)
btn_plot.pack(pady=5)

# Run the app
app.mainloop()
