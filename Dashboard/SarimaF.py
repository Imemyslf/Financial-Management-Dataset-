import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Function to load and preprocess data
def load_data(df):
    if df.empty or len(df.columns) < 4:
        return None, "Excel file is empty or has insufficient columns. Ensure it has a date column (first column) and columns 'Net profit/(loss) for the period', 'Total Revenue', 'Total Expenditure'."
    
    # Dynamically use the first column as the date column
    date_column = df.columns[0]
    
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

# Function to run the SARIMA model
def run_sarima_model(df):
    # Feature engineering
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
    
    # Prepare exogenous variables
    exog_vars = ["revenue", "total_expenditure", "revenue_expenditure"]
    exog_train = train_df[exog_vars]
    exog_test = test_df[exog_vars]
    
    # SARIMA model
    order = (1, 1, 1)  # ARIMA component
    seasonal_order = (1, 1, 1, 4)  # Seasonal component with quarterly seasonality (s=4)
    sarima_model = SARIMAX(
        train_df["y"],
        exog=exog_train,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    ).fit(disp=False)
    
    # Predictions
    train_pred = sarima_model.predict(start=0, end=len(train_df)-1, exog=exog_train)
    test_pred = sarima_model.predict(
        start=len(train_df), end=len(df)-1, exog=exog_test
    )
    
    # Store predictions
    train_df["sarima_pred"] = train_pred
    test_df["sarima_pred"] = test_pred
    
    # Evaluate
    mae = mean_absolute_error(test_df["y"], test_df["sarima_pred"])
    mse = mean_squared_error(test_df["y"], test_df["sarima_pred"])
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((test_df["y"] - test_df["sarima_pred"]) / test_df["y"])) * 100
    
    metrics = {
        "mae": mae,
        "rmse": rmse,
        "mape": mape
    }
    
    # Forecast next 8 quarters
    future = pd.DataFrame()
    future["ds"] = pd.date_range(start=df["ds"].iloc[-1], periods=9, freq="QE")[1:]
    
    # Forecast exogenous variables
    revenue_model = ExponentialSmoothing(df["revenue"], trend="add", seasonal="add", seasonal_periods=4).fit()
    expenditure_model = ExponentialSmoothing(df["total_expenditure"], trend="add", seasonal="add", seasonal_periods=4).fit()
    future["revenue"] = revenue_model.forecast(8).values
    future["total_expenditure"] = expenditure_model.forecast(8).values
    future["revenue_expenditure"] = future["revenue"] * future["total_expenditure"]
    
    # Prepare exogenous variables for forecasting
    exog_future = future[exog_vars]
    
    # SARIMA forecast
    sarima_forecast = sarima_model.forecast(steps=8, exog=exog_future)
    future["yhat"] = sarima_forecast.values
    
    # Confidence intervals (approximate)
    forecast_obj = sarima_model.get_forecast(steps=8, exog=exog_future)
    conf_int = forecast_obj.conf_int(alpha=0.2)  # 80% CI
    future["yhat_lower"] = conf_int.iloc[:, 0].values
    future["yhat_upper"] = conf_int.iloc[:, 1].values
    
    # Return results
    return {
        "train_df": train_df,
        "test_df": test_df,
        "future_df": future[["ds", "yhat", "yhat_lower", "yhat_upper"]],
        "metrics": metrics
    }