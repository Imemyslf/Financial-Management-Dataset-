# import json
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# import os

# # Load data
# current_dir = os.getcwd()
# path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")
# with open(path) as f:
#     data = json.load(f)

# # Extract net profit for each quarter and prepare DataFrame
# quarters = data["Total Profit for each quarter"]
# profit_data = [quarters[q]["Profit"] for q in sorted(quarters.keys())]
# quarter_names = list(sorted(quarters.keys()))  # Get sorted quarter names

# # Convert to DataFrame
# df = pd.DataFrame(profit_data, columns=["Net Profit"])

# # Normalize the data
# scaler = MinMaxScaler(feature_range=(0, 1))
# df_scaled = scaler.fit_transform(df)

# # Split data into train, test, and manual input sets
# train_size = int(len(df_scaled) * 0.6)
# test_size = int(len(df_scaled) * 0.2)
# manual_input_size = len(df_scaled) - train_size - test_size

# train_data = df_scaled[:train_size]
# test_data = df_scaled[train_size:train_size + test_size]
# manual_input_data = df_scaled[train_size + test_size:]

# # Split quarters for train, test, and manual input
# train_quarters = quarter_names[:train_size]
# test_quarters = quarter_names[train_size:train_size + test_size]
# manual_input_quarters = quarter_names[train_size + test_size:]



# # Prepare training data for LSTM from the train set
# sequence_length = 4  # Number of past quarters to consider
# X_train, y_train = [], []

# for i in range(len(train_data) - sequence_length):
#     X_train.append(train_data[i:i+sequence_length, 0])
#     y_train.append(train_data[i + sequence_length, 0])

# X_train, y_train = np.array(X_train), np.array(y_train)
# X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))  # Reshape for LSTM [samples, time steps, features]

# # Prepare testing data for LSTM from the test set
# X_test, y_test = [], []

# for i in range(len(test_data) - sequence_length):
#     X_test.append(test_data[i:i+sequence_length, 0])
#     y_test.append(test_data[i + sequence_length, 0])

# X_test, y_test = np.array(X_test), np.array(y_test)
# X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))  # Reshape for LSTM

# # Build LSTM model
# model = Sequential()
# model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
# model.add(LSTM(units=50, return_sequences=False))
# model.add(Dense(units=25))
# model.add(Dense(units=1))

# # Compile the model
# model.compile(optimizer='adam', loss='mean_squared_error')

# # Train the model
# model.fit(X_train, y_train, batch_size=1, epochs=50)

# # Test the model
# test_predictions = model.predict(X_test)
# test_predictions = scaler.inverse_transform(test_predictions)  # Convert back to original scale
# y_test_rescaled = scaler.inverse_transform([y_test])  # Original scale for comparison

# # Calculate test loss
# test_loss = model.evaluate(X_test, y_test)
# print(f"Test Loss (MSE): {test_loss}")

# # Predict next quarter's net profit using the last sequence of test data
# last_sequence = df_scaled[-sequence_length:]  # Take the last sequence from the data
# last_sequence = last_sequence.reshape((1, sequence_length, 1))  # Reshape for prediction

# predicted_profit = model.predict(last_sequence)
# predicted_profit = scaler.inverse_transform(predicted_profit)  # Convert back to original scale

# print(f"Predicted Net Profit for the next quarter: {predicted_profit[0][0]:.2f}")

# # Display quarters for each set
# print("Training Quarters:", train_quarters)
# print("Testing Quarters:", test_quarters)
# print("Manual Input Quarters (Unused):", manual_input_quarters)

import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os

# Load data
current_dir = os.getcwd()
path = os.path.join(current_dir, "Companies", "IT Services & Consulting", "Infosys Ltd", "Infosys Ltd_total_revenue.json")
with open(path) as f:
    data = json.load(f)

# Extract net profit for each quarter and prepare DataFrame
quarters = data["Total Profit for each quarter"]
profit_data = [quarters[q]["Profit"] for q in sorted(quarters.keys())]
quarter_names = list(sorted(quarters.keys()))  # Get sorted quarter names

# Convert to DataFrame
df = pd.DataFrame(profit_data, columns=["Net Profit"])

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
df_scaled = scaler.fit_transform(df)

# Split data into train, test, and manual input sets
train_size = int(len(df_scaled) * 0.6)
test_size = int(len(df_scaled) * 0.2)
manual_input_size = len(df_scaled) - train_size - test_size

train_data = df_scaled[:train_size]
test_data = df_scaled[train_size:train_size + test_size]
manual_input_data = df_scaled[train_size + test_size:]

# Split quarters for train, test, and manual input
train_quarters = quarter_names[:train_size]
test_quarters = quarter_names[train_size:train_size + test_size]
manual_input_quarters = quarter_names[train_size + test_size:]

# Prepare training data for LSTM from the train set
sequence_length = 4  # Number of past quarters to consider
X_train, y_train = [], []

for i in range(len(train_data) - sequence_length):
    X_train.append(train_data[i:i+sequence_length, 0])
    y_train.append(train_data[i + sequence_length, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))  # Reshape for LSTM [samples, time steps, features]

# Prepare testing data for LSTM from the test set
X_test, y_test = [], []

for i in range(len(test_data) - sequence_length):
    X_test.append(test_data[i:i+sequence_length, 0])
    y_test.append(test_data[i + sequence_length, 0])

X_test, y_test = np.array(X_test), np.array(y_test)
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))  # Reshape for LSTM

# Build LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, batch_size=1, epochs=50)

# Test the model
test_predictions = model.predict(X_test)
test_predictions = scaler.inverse_transform(test_predictions)  # Convert back to original scale
y_test_rescaled = scaler.inverse_transform([y_test])  # Original scale for comparison

# Calculate test loss
test_loss = model.evaluate(X_test, y_test)
print(f"Test Loss (MSE): {test_loss}")

# Predict next quarter's net profit using the last sequence of test data
last_sequence = df_scaled[-sequence_length:]  # Take the last sequence from the data
last_sequence = last_sequence.reshape((1, sequence_length, 1))  # Reshape for prediction

predicted_profit = model.predict(last_sequence)
predicted_profit = scaler.inverse_transform(predicted_profit)  # Convert back to original scale

print(f"Predicted Net Profit for the next quarter: {predicted_profit[0][0]:.2f}")

# Display quarters for each set
print("Training Quarters:", train_quarters)
print("Testing Quarters:", test_quarters)
print("Manual Input Quarters (Unused):", manual_input_quarters)

# Define function to test the prediction model
def test_prediction_model(model, data, scaler, sequence_length=4):
    """
    Tests the prediction model on provided data.
    
    Parameters:
    - model: The trained LSTM model.
    - data: The scaled data to test the model on.
    - scaler: The scaler used to normalize the data.
    - sequence_length: Number of previous data points used for prediction (default is 4).
    
    Returns:
    - A list of predicted values and the corresponding actual values (if available).
    """
    # Prepare the test sequences from the data
    X_test, y_actual = [], []

    for i in range(len(data) - sequence_length):
        X_test.append(data[i:i + sequence_length, 0])
        y_actual.append(data[i + sequence_length, 0])

    # Convert lists to numpy arrays and reshape for LSTM input
    X_test = np.array(X_test)
    y_actual = np.array(y_actual)
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))  # Reshape for LSTM

    # Predict using the model
    predictions = model.predict(X_test)
    
    # Rescale predictions and actual values to original scale
    predictions_rescaled = scaler.inverse_transform(predictions)
    y_actual_rescaled = scaler.inverse_transform([y_actual]).flatten()

    # Calculate the mean squared error for evaluation
    mse = np.mean((predictions_rescaled.flatten() - y_actual_rescaled) ** 2)
    print(f"Mean Squared Error on Test Data: {mse:.4f}")
    
    # Display predictions and actual values
    for i in range(len(predictions_rescaled)):
        print(f"Predicted: {predictions_rescaled[i][0]:.2f}, Actual: {y_actual_rescaled[i]:.2f}")

    return predictions_rescaled, y_actual_rescaled

# Test the model on the test data set
predicted_values, actual_values = test_prediction_model(model, test_data, scaler, sequence_length=4)
