# import xgboost as xgb
# from sklearn.metrics import mean_absolute_error
# from sklearn.preprocessing import StandardScaler
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # Date parsing function (MISSING IN YOUR ORIGINAL CODE)
# def parse_quarter(date_str):
#     """Parse quarterly date strings into datetime objects"""
#     month_map = {"Mar": ("03", "31"), "Jun": ("06", "30"), "Sep": ("09", "30"), "Dec": ("12", "31")}
#     parts = date_str.split()
#     year = "20" + parts[1] if int(parts[1]) < 25 else "19" + parts[1]
#     month, day = month_map[parts[0]]
#     return pd.to_datetime(f"{year}-{month}-{day}")

# # Feature Engineering function
# def create_features(df):
#     """Create time-series features from datetime index"""
#     df = df.copy()
    
#     # Basic time features
#     df['quarter'] = df['ds'].dt.quarter
#     df['year'] = df['ds'].dt.year
    
#     # Lag features
#     for lag in [1, 2, 3, 4]:  # Including 4 quarters (1 year) of lags
#         df[f'lag_{lag}'] = df['y'].shift(lag)
    
#     # Rolling statistics
#     df['rolling_mean_4'] = df['y'].rolling(window=4).mean()  # 1-year rolling mean
#     df['rolling_std_4'] = df['y'].rolling(window=4).std()   # 1-year rolling std
#     df['rolling_min_4'] = df['y'].rolling(window=4).min()    # 1-year rolling min
#     df['rolling_max_4'] = df['y'].rolling(window=4).max()    # 1-year rolling max
    
#     # Financial ratios
#     df['profit_margin'] = df['y'] / df['revenue']
#     df['expense_ratio'] = df['total_expenditure'] / df['revenue']
    
#     # Trend features
#     df['trend'] = np.arange(len(df))
#     df['trend_squared'] = df['trend'] ** 2
    
#     # Interaction terms
#     df['revenue_expenditure'] = df['revenue'] * df['total_expenditure']
    
#     return df

# # Load and prepare data
# file_path = "C:/Users/Aditya/Desktop/FyPro/Companies/Updated/3i infotech_Sorted_Quarterly_Data.xlsx"
# df = pd.read_excel(file_path, sheet_name="Sheet1")

# # Rename columns
# df.rename(columns={
#     "Quarterly Results of 3i Infotech(in Rs. Cr.)": "ds",
#     "Net profit/(loss) for the period": "y",
#     "Total Revenue": "revenue",
#     "Total Expenditure": "total_expenditure"  # Fixed typo from original (Expenditure vs Expenditure)
# }, inplace=True)

# # Parse dates using the function we defined
# df["ds"] = df["ds"].apply(parse_quarter)

# # Feature engineering
# df = create_features(df)

# # Handle missing values (from lag features)
# df = df.dropna()

# # Train-test split
# train_size = len(df) - 10  # Last 10 quarters for testing
# train_df = df.iloc[:train_size].copy()
# test_df = df.iloc[train_size:].copy()

# # Select features
# features = [
#     'quarter', 'year',
#     'lag_1', 'lag_2', 'lag_3', 'lag_4',
#     'rolling_mean_4', 'rolling_std_4', 
#     'rolling_min_4', 'rolling_max_4',
#     'profit_margin', 'expense_ratio',
#     'trend', 'trend_squared',
#     'revenue', 'total_expenditure',
#     'revenue_expenditure'
# ]

# X_train = train_df[features]
# y_train = train_df['y']
# X_test = test_df[features]
# y_test = test_df['y']

# # Scale features
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# # XGBoost model configuration
# params = {
#     'objective': 'reg:squarederror',
#     'max_depth': 4,
#     'learning_rate': 0.05,
#     'subsample': 0.8,
#     'colsample_bytree': 0.8,
#     'gamma': 0.1,
#     'min_child_weight': 1,
#     'eval_metric': 'mae',
#     'n_estimators': 500,
#     'early_stopping_rounds': 20,
#     'random_state': 42
# }

# # Create and train model
# xgb_model = xgb.XGBRegressor(**params)
# xgb_model.fit(
#     X_train_scaled, 
#     y_train,
#     eval_set=[(X_train_scaled, y_train), (X_test_scaled, y_test)],
#     verbose=10
# )

# # Make predictions
# train_pred = xgb_model.predict(X_train_scaled)
# test_pred = xgb_model.predict(X_test_scaled)

# # Evaluate
# train_mae = mean_absolute_error(y_train, train_pred)
# test_mae = mean_absolute_error(y_test, test_pred)
# print(f"\nTraining MAE: {train_mae:.2f}")
# print(f"Test MAE: {test_mae:.2f}")

# # Plot feature importance
# plt.figure(figsize=(10, 6))
# xgb.plot_importance(xgb_model, importance_type='gain', max_num_features=15)
# plt.title('XGBoost Feature Importance (Gain)')
# plt.tight_layout()
# plt.show()

# # Plot actual vs predicted
# plt.figure(figsize=(12, 6))
# plt.plot(train_df['ds'], y_train, label='Training Actual', color='blue')
# plt.plot(test_df['ds'], y_test, label='Test Actual', color='green')
# plt.plot(train_df['ds'], train_pred, label='Training Predicted', color='red', linestyle='--')
# plt.plot(test_df['ds'], test_pred, label='Test Predicted', color='orange', linestyle='--')
# plt.title('XGBoost: Actual vs Predicted Net Profit')
# plt.xlabel('Date')
# plt.ylabel('Net Profit (Rs. Cr.)')
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()









# import xgboost as xgb
# from sklearn.metrics import mean_absolute_error
# from sklearn.preprocessing import StandardScaler
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # Date parsing function
# def parse_quarter(date_str):
#     """Parse quarterly date strings into datetime objects"""
#     month_map = {"Mar": ("03", "31"), "Jun": ("06", "30"), "Sep": ("09", "30"), "Dec": ("12", "31")}
#     parts = date_str.split()
#     year = "20" + parts[1] if int(parts[1]) < 25 else "19" + parts[1]
#     month, day = month_map[parts[0]]
#     return pd.to_datetime(f"{year}-{month}-{day}")

# # Feature Engineering function
# def create_features(df):
#     """Create time-series features from datetime index"""
#     df = df.copy()
    
#     # Basic time features
#     df['quarter'] = df['ds'].dt.quarter
#     df['year'] = df['ds'].dt.year
    
#     # Lag features
#     for lag in [1, 2, 3, 4]:  # Including 4 quarters (1 year) of lags
#         df[f'lag_{lag}'] = df['y'].shift(lag)
    
#     # Rolling statistics
#     df['rolling_mean_4'] = df['y'].rolling(window=4).mean()  # 1-year rolling mean
#     df['rolling_std_4'] = df['y'].rolling(window=4).std()   # 1-year rolling std
#     df['rolling_min_4'] = df['y'].rolling(window=4).min()    # 1-year rolling min
#     df['rolling_max_4'] = df['y'].rolling(window=4).max()    # 1-year rolling max
    
#     # Financial ratios
#     df['profit_margin'] = df['y'] / df['revenue']
#     df['expense_ratio'] = df['total_expenditure'] / df['revenue']
    
#     # Trend features
#     df['trend'] = np.arange(len(df))
#     df['trend_squared'] = df['trend'] ** 2
    
#     # Interaction terms
#     df['revenue_expenditure'] = df['revenue'] * df['total_expenditure']
    
#     return df

# # Function to forecast future values iteratively
# def forecast_future(model, scaler, last_row, features, periods=8):
#     """Forecast future periods iteratively"""
#     future_predictions = []
#     future_dates = pd.date_range(
#         start=last_row['ds'] + pd.offsets.QuarterBegin(),
#         periods=periods,
#         freq='QE'
#     )
    
#     # Initialize with last available data
#     current_data = last_row[features].copy()
    
#     for i in range(periods):
#         # Prepare features for prediction
#         features_df = pd.DataFrame([current_data], columns=features)
#         features_scaled = scaler.transform(features_df)
        
#         # Make prediction
#         pred = model.predict(features_scaled)[0]
#         future_predictions.append(pred)
        
#         # Update features for next prediction
#         # Shift lag features
#         for lag in range(4, 1, -1):
#             current_data[f'lag_{lag}'] = current_data[f'lag_{lag-1}']
#         current_data['lag_1'] = pred
        
#         # Update rolling statistics (simplified approach)
#         current_lags = [current_data[f'lag_{i}'] for i in range(1, 5)]
#         current_data['rolling_mean_4'] = np.mean(current_lags)
#         current_data['rolling_std_4'] = np.std(current_lags)
#         current_data['rolling_min_4'] = min(current_lags)
#         current_data['rolling_max_4'] = max(current_lags)
        
#         # Update trend
#         current_data['trend'] += 1
#         current_data['trend_squared'] = current_data['trend'] ** 2
        
#         # Update financial ratios (using last known values for simplicity)
#         current_data['profit_margin'] = pred / current_data['revenue']
#         current_data['expense_ratio'] = current_data['total_expenditure'] / current_data['revenue']
        
#     return future_dates, future_predictions

# # Load and prepare data
# file_path = "C:/Users/Aditya/Desktop/FyPro/Companies/Updated/3i infotech_Sorted_Quarterly_Data.xlsx"
# df = pd.read_excel(file_path, sheet_name="Sheet1")

# # Rename columns
# df.rename(columns={
#     "Quarterly Results of 3i Infotech(in Rs. Cr.)": "ds",
#     "Net profit/(loss) for the period": "y",
#     "Total Revenue": "revenue",
#     "Total Expenditure": "total_expenditure"
# }, inplace=True)

# # Parse dates
# df["ds"] = df["ds"].apply(parse_quarter)

# # Feature engineering
# df = create_features(df)

# # Handle missing values
# df = df.dropna()

# # Train-test split
# train_size = len(df) - 10  # Last 10 quarters for testing
# train_df = df.iloc[:train_size].copy()
# test_df = df.iloc[train_size:].copy()

# # Select features
# features = [
#     'quarter', 'year',
#     'lag_1', 'lag_2', 'lag_3', 'lag_4',
#     'rolling_mean_4', 'rolling_std_4', 
#     'rolling_min_4', 'rolling_max_4',
#     'profit_margin', 'expense_ratio',
#     'trend', 'trend_squared',
#     'revenue', 'total_expenditure',
#     'revenue_expenditure'
# ]

# X_train = train_df[features]
# y_train = train_df['y']
# X_test = test_df[features]
# y_test = test_df['y']

# # Scale features
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# # XGBoost model configuration
# params = {
#     'objective': 'reg:squarederror',
#     'max_depth': 4,
#     'learning_rate': 0.05,
#     'subsample': 0.8,
#     'colsample_bytree': 0.8,
#     'gamma': 0.1,
#     'min_child_weight': 1,
#     'eval_metric': 'mae',
#     'n_estimators': 500,
#     'early_stopping_rounds': 20,
#     'random_state': 42
# }

# # Create and train model
# xgb_model = xgb.XGBRegressor(**params)
# xgb_model.fit(
#     X_train_scaled, 
#     y_train,
#     eval_set=[(X_train_scaled, y_train), (X_test_scaled, y_test)],
#     verbose=10
# )

# # Make predictions
# train_pred = xgb_model.predict(X_train_scaled)
# test_pred = xgb_model.predict(X_test_scaled)

# # Evaluate
# train_mae = mean_absolute_error(y_train, train_pred)
# test_mae = mean_absolute_error(y_test, test_pred)
# print(f"\nTraining MAE: {train_mae:.2f}")
# print(f"Test MAE: {test_mae:.2f}")

# # Forecast next 8 quarters
# last_row = df.iloc[-1][features + ['ds']]  # Get last available data point
# future_dates, future_predictions = forecast_future(xgb_model, scaler, last_row, features, periods=8)

# # Create a DataFrame for future predictions
# future_df = pd.DataFrame({
#     'ds': future_dates,
#     'y_pred': future_predictions,
#     'type': 'forecast'
# })

# # Plot actual vs predicted with forecast
# plt.figure(figsize=(14, 7))
# plt.plot(df['ds'], df['y'], label='Historical Actual', color='blue')
# plt.plot(test_df['ds'], test_pred, label='Test Predictions', color='orange', linestyle='--')
# plt.plot(future_df['ds'], future_df['y_pred'], label='8-Quarter Forecast', color='green', marker='o')

# plt.title('3i Infotech Net Profit: History and 8-Quarter Forecast')
# plt.xlabel('Date')
# plt.ylabel('Net Profit (Rs. Cr.)')
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # Print forecast results
# print("\n8-Quarter Forecast:")
# print(future_df[['ds', 'y_pred']].rename(columns={'ds': 'Quarter', 'y_pred': 'Net Profit (Rs. Cr.)'}).to_string(index=False))

# # Plot feature importance
# plt.figure(figsize=(10, 6))
# xgb.plot_importance(xgb_model, importance_type='gain', max_num_features=15)
# plt.title('XGBoost Feature Importance (Gain)')
# plt.tight_layout()
# plt.show()







import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration
CONFIG = {
    'test_size': 10,
    'forecast_periods': 8,
    'random_state': 42
}

def parse_quarter(date_str):
    """Parse quarterly date strings into datetime objects"""
    month_map = {"Mar": ("03", "31"), "Jun": ("06", "30"), "Sep": ("09", "30"), "Dec": ("12", "31")}
    parts = date_str.split()
    year = "20" + parts[1] if int(parts[1]) < 25 else "19" + parts[1]
    month, day = month_map[parts[0]]
    return pd.to_datetime(f"{year}-{month}-{day}")

def create_features(df):
    """Create time-series features from datetime index"""
    df = df.copy()
    
    # Time features with seasonality
    df['quarter_num'] = df['ds'].dt.quarter
    df['quarter_sin'] = np.sin(2 * np.pi * df['quarter_num']/4)
    df['quarter_cos'] = np.cos(2 * np.pi * df['quarter_num']/4)
    df['year'] = df['ds'].dt.year
    
    # Lag features with decay
    for lag in [1, 2, 3, 4]:
        df[f'lag_{lag}'] = df['y'].shift(lag) * (0.9 ** lag)  # Decaying effect
    
    # Rolling statistics
    df['rolling_mean_4'] = df['y'].rolling(window=4, min_periods=2).mean()
    df['rolling_std_4'] = df['y'].rolling(window=4, min_periods=2).std().fillna(0)
    
    # Financial ratios with clipping
    df['profit_margin'] = np.clip(df['y'] / (df['revenue'] + 1e-6), -2, 2)
    df['expense_ratio'] = np.clip(df['total_expenditure'] / (df['revenue'] + 1e-6), 0.5, 1.5)
    
    # Conservative trend
    df['trend'] = np.arange(len(df)) / 100  # Small coefficient
    
    return df.dropna()

def forecast_future(model, scaler, last_row, features, periods=8):
    """Forecast future periods with natural fluctuations"""
    future_predictions = []
    future_dates = pd.date_range(
        start=last_row['ds'] + pd.offsets.QuarterBegin(),
        periods=periods,
        freq='QE'
    )
    
    current_data = last_row[features].copy()
    revenue = current_data['revenue']
    expenditure = current_data['total_expenditure']
    
    for i in range(periods):
        # Update seasonal features
        current_quarter = (current_data['quarter_num'] + 1) % 4 or 4
        current_data['quarter_sin'] = np.sin(2 * np.pi * current_quarter/4)
        current_data['quarter_cos'] = np.cos(2 * np.pi * current_quarter/4)
        current_data['quarter_num'] = current_quarter
        
        # Add small business fluctuations
        revenue *= np.random.normal(1.02, 0.03)  # ~2% growth with 3% std dev
        expenditure *= np.random.normal(1.015, 0.02)
        
        current_data['revenue'] = revenue
        current_data['total_expenditure'] = expenditure
        current_data['profit_margin'] = np.clip(current_data['lag_1'] / revenue, -2, 2)
        current_data['expense_ratio'] = np.clip(expenditure / revenue, 0.5, 1.5)
        
        # Scale and predict with small noise
        features_scaled = scaler.transform(pd.DataFrame([current_data], columns=features))
        pred = model.predict(features_scaled)[0] * np.random.normal(1, 0.02)
        future_predictions.append(pred)
        
        # Update features for next period
        for lag in range(4, 1, -1):
            current_data[f'lag_{lag}'] = current_data[f'lag_{lag-1}'] * 0.9  # Decay
        current_data['lag_1'] = pred * 0.9
        
        # Update rolling stats
        current_lags = [current_data[f'lag_{i}'] for i in range(1,5)]
        current_data['rolling_mean_4'] = np.mean(current_lags)
        current_data['rolling_std_4'] = np.std(current_lags)
        
        # Update trend
        current_data['trend'] += 0.01
        
    return future_dates, future_predictions

# Load and prepare data
file_path = "C:/Users/Aditya/Desktop/FyPro/Companies/Updated/TCS_Sorted_Quarterly_Data.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Rename columns
df.rename(columns={
    "Quarterly Results of Tata Consultancy Services(in Rs. Cr.)": "ds",
    "Net profit/(loss) for the period": "y",
    "Total Revenue": "revenue",
    "Total Expenditure": "total_expenditure"
}, inplace=True)

# Parse dates and create features
df["ds"] = df["ds"].apply(parse_quarter)
df = create_features(df)

# Train-test split
train_size = len(df) - CONFIG['test_size']
train_df = df.iloc[:train_size].copy()
test_df = df.iloc[train_size:].copy()

# Feature selection
features = [
    'quarter_num', 'quarter_sin', 'quarter_cos',
    'lag_1', 'lag_2', 'lag_3', 'lag_4',
    'rolling_mean_4', 'rolling_std_4',
    'profit_margin', 'expense_ratio',
    'trend', 'revenue', 'total_expenditure'
]

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(train_df[features])
X_test = scaler.transform(test_df[features])
y_train, y_test = train_df['y'].values, test_df['y'].values

# XGBoost model with regularization
params = {
    'objective': 'reg:squarederror',
    'max_depth': 3,
    'learning_rate': 0.03,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'gamma': 0.2,
    'min_child_weight': 3,
    'alpha': 0.1,  # L1 regularization
    'lambda': 0.3,  # L2 regularization
    'n_estimators': 500,
    'random_state': CONFIG['random_state']
}

model = xgb.XGBRegressor(**params)
model.fit(X_train, y_train)

# Evaluate
train_pred = model.predict(X_train)
test_pred = model.predict(X_test)
print(f"Training MAE: {mean_absolute_error(y_train, train_pred):.2f}")
print(f"Test MAE: {mean_absolute_error(y_test, test_pred):.2f}")

# Forecast future
last_row = df.iloc[-1][features + ['ds']]
future_dates, future_values = forecast_future(model, scaler, last_row, features)

# Plot results
plt.figure(figsize=(14, 7))
plt.plot(df['ds'], df['y'], 'b-', label='Historical')
plt.plot(test_df['ds'], test_df['y'], 'g-', label='Actual Test')
plt.plot(test_df['ds'], test_pred, 'r--', label='Test Predictions')
plt.plot(future_dates, future_values, 'ko-', label='Forecast')
plt.title('3i Infotech Net Profit Forecast with Fluctuations')
plt.xlabel('Quarter')
plt.ylabel('Net Profit (Rs. Cr.)')
plt.legend()
plt.grid(True)
plt.show()

# Print forecast
forecast_df = pd.DataFrame({
    'Quarter': future_dates,
    'Net Profit (Rs. Cr.)': np.round(future_values, 2)
})
print("\n8-Quarter Forecast with Natural Fluctuations:")
print(forecast_df.to_string(index=False))