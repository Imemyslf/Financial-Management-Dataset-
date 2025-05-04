import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# Function to load and preprocess data
def load_data(df):
    if df.empty or len(df.columns) < 4:
        return None, "Excel file is empty or has insufficient columns. Ensure it has a date column (first column) and columns 'Net profit/(loss) for the period', 'Total Revenue', 'Total Expenditure'."
    
    # Dynamically use the first column as the date column
    date_column = df.columns[0]
    
    # Debug: Log first few values
    print(f"Sample values in first column ('{date_column}'): {df[date_column].head().tolist()}")
    
    # Define required columns
    required_columns = {
        "Net profit/(loss) for the period": "y",
        "Total Revenue": "revenue",
        "Total Expenditure": "total_expenditure"
    }
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return None, f"Missing required columns: {', '.join(missing_columns)}. Ensure the file includes 'Net profit/(loss) for the period', 'Total Revenue', 'Total Expenditure'."
    
    # Rename columns
    rename_dict = {date_column: "ds", **required_columns}
    df = df.rename(columns=rename_dict)
    
    # Parse dates
    def parse_quarter(date_str):
        month_map = {"mar": ("03", "31"), "jun": ("06", "30"), "sep": ("09", "30"), "dec": ("12", "31")}
        date_str = str(date_str).strip().lower()  # Handle spaces and case
        parts = date_str.split()
        if len(parts) < 2:
            return pd.NaT
        month = parts[0]
        year_suffix = parts[1]
        if month not in month_map:
            return pd.NaT
        try:
            year = "20" + year_suffix if int(year_suffix) <= 50 else "19" + year_suffix
            month, day = month_map[month]
            return pd.to_datetime(f"{year}-{month}-{day}")
        except:
            return pd.NaT
    
    df["ds"] = df["ds"].apply(parse_quarter)
    if df["ds"].isna().all():
        invalid_dates = df["ds"].index[df["ds"].isna()]
        sample_invalid = df.loc[invalid_dates, "ds"].head().tolist()
        return None, f"Failed to parse dates in the first column ('{date_column}'). Ensure format is like 'Mar 05 Q4'. Sample invalid values: {sample_invalid}"
    df = df.dropna(subset=["ds"]).sort_values("ds")
    
    return df, None

# Function to run the hybrid model
def run_hybrid_model(df):
    # Feature engineering
    df["trend"] = np.arange(len(df))
    for lag in [1, 2, 3]:
        df[f"lag_{lag}"] = df["y"].shift(lag)
    df["rolling_mean"] = df["y"].rolling(window=4, min_periods=1).mean()
    df["rolling_std"] = df["y"].rolling(window=4, min_periods=1).std()
    df["revenue_expenditure"] = df["revenue"] * df["total_expenditure"]
    
    # Handle missing values
    df = df.ffill().bfill()
    
    # Cap outliers
    q1, q3 = np.percentile(df["y"], [25, 75])
    iqr = q3 - q1
    lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    df["y"] = df["y"].clip(lower_bound, upper_bound)
    
    # Train-test split
    train_size = len(df) - 10
    train_df = df.iloc[:train_size].copy()
    test_df = df.iloc[train_size:].copy()
    dates_train, dates_test = train_df["ds"], test_df["ds"]
    
    # Prophet model
    prophet_df = train_df[["ds", "y"]].copy()
    prophet_df["revenue"] = train_df["revenue"]
    prophet_df["total_expenditure"] = train_df["total_expenditure"]
    
    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode="additive"
    )
    prophet_model.add_regressor("revenue")
    prophet_model.add_regressor("total_expenditure")
    prophet_model.fit(prophet_df)
    
    # Prophet predictions
    prophet_train_pred = prophet_model.predict(prophet_df)
    train_df["prophet_pred"] = prophet_train_pred["yhat"].values
    
    prophet_test_df = test_df[["ds", "revenue", "total_expenditure"]].copy()
    prophet_test_pred = prophet_model.predict(prophet_test_df)
    test_df["prophet_pred"] = prophet_test_pred["yhat"].values
    
    # Compute residuals
    train_df["residual"] = train_df["y"] - train_df["prophet_pred"]
    test_df["residual"] = test_df["y"] - test_df["prophet_pred"]
    
    # Features for XGBoost
    features = ["trend", "lag_1", "lag_2", "lag_3", "rolling_mean", "revenue", "total_expenditure", "revenue_expenditure"]
    X_train = train_df[features]
    y_train_residual = train_df["residual"].replace([np.inf, -np.inf], np.nan).fillna(0)
    X_test = test_df[features]
    y_test_residual = test_df["residual"].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=features, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=features, index=X_test.index)
    
    # XGBoost model
    params = {
        "objective": "reg:squarederror",
        "max_depth": 3,
        "learning_rate": 0.2,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "eval_metric": "mae",
        "random_state": 42
    }
    xgb_model = xgb.XGBRegressor(**params)
    xgb_model.fit(X_train_scaled, y_train_residual)
    
    # Predict residuals
    xgb_train_residual_pred = xgb_model.predict(X_train_scaled)
    xgb_test_residual_pred = xgb_model.predict(X_test_scaled)
    
    # Final predictions
    train_df["final_pred"] = train_df["prophet_pred"] + xgb_train_residual_pred
    test_df["final_pred"] = test_df["prophet_pred"] + xgb_test_residual_pred
    
    # Ensure no NaN values in predictions
    test_df["final_pred"] = test_df["final_pred"].fillna(test_df["prophet_pred"])
    
    # Evaluate
    mae = mean_absolute_error(test_df["y"], test_df["final_pred"])
    mse = mean_squared_error(test_df["y"], test_df["final_pred"])
    rmse = np.sqrt(mse)
    r2 = r2_score(test_df["y"], test_df["final_pred"])
    mape = np.mean(np.abs((test_df["y"] - test_df["final_pred"]) / test_df["y"])) * 100
    
    metrics = {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "mape": mape
    }
    
    # Forecast next 8 quarters
    future = pd.DataFrame()
    future["ds"] = pd.date_range(start=df["ds"].iloc[-1], periods=9, freq="QE")[1:]
    
    # Forecast revenue and expenditure
    revenue_model = ExponentialSmoothing(df["revenue"], trend="add", seasonal="add", seasonal_periods=4).fit()
    expenditure_model = ExponentialSmoothing(df["total_expenditure"], trend="add", seasonal="add", seasonal_periods=4).fit()
    future["revenue"] = revenue_model.forecast(8).values
    future["total_expenditure"] = expenditure_model.forecast(8).values
    
    prophet_future_pred = prophet_model.predict(future)
    future["prophet_pred"] = prophet_future_pred["yhat"].values
    future["yhat_lower"] = prophet_future_pred["yhat_lower"].values
    future["yhat_upper"] = prophet_future_pred["yhat_upper"].values
    
    # Prepare future features
    future["trend"] = np.arange(len(df), len(df) + 8)
    for lag in [1, 2, 3]:
        future[f"lag_{lag}"] = np.nan
    
    # Initialize with last known values
    future.loc[future.index[0], "lag_1"] = df["y"].iloc[-1]
    future.loc[future.index[0], "lag_2"] = df["y"].iloc[-2]
    future.loc[future.index[0], "lag_3"] = df["y"].iloc[-3]
    
    future["rolling_mean"] = df["y"].rolling(window=4).mean().iloc[-1]
    future["revenue_expenditure"] = future["revenue"] * future["total_expenditure"]
    
    # Fill any remaining NAs
    future = future.ffill().bfill()
    
    # Scale future features
    future_scaled = scaler.transform(future[features])
    future_scaled = pd.DataFrame(future_scaled, columns=features, index=future.index)
    
    # Make predictions iteratively
    predictions = []
    for i in range(8):
        row = future_scaled.iloc[i:i+1].copy()
        residual_pred = xgb_model.predict(row)[0]
        pred = future["prophet_pred"].iloc[i] + residual_pred
        predictions.append(pred)
        
        # Update lags for next prediction if not last iteration
        if i < 7:
            future_scaled.iloc[i+1, future_scaled.columns.get_loc("lag_1")] = pred
            future_scaled.iloc[i+1, future_scaled.columns.get_loc("lag_2")] = future_scaled.iloc[i, future_scaled.columns.get_loc("lag_1")]
            future_scaled.iloc[i+1, future_scaled.columns.get_loc("lag_3")] = future_scaled.iloc[i, future_scaled.columns.get_loc("lag_2")]
    
    future["yhat"] = predictions
    
    # Return results
    return {
        "train_df": train_df,
        "test_df": test_df,
        "future_df": future[["ds", "yhat", "yhat_lower", "yhat_upper"]],
        "metrics": metrics
    }