import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
import base64
import os
import google.generativeai as genai
from HybridF import load_data as load_data_hybrid, run_hybrid_model
from SarimaF import load_data as load_data_sarima, run_sarima_model
from Heatmap import run_heatmap_dashboard
from SankeyF import run_sankey_diagram

# Streamlit app configuration
st.set_page_config(page_title="ARK Financial Dashboards", layout="wide")

# Configure Gemini API
try:
    genai.configure(api_key="AIzaSyAZpmw8Qwx457X3M9N09EP9FSaBoOhvK-g")
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.warning(f"Failed to configure Gemini API: {str(e)}. LLM insights will not be available.")

# Function to validate the uploaded file
def validate_file(df):
    if df.empty or len(df.columns) < 2:
        return False, "Excel file is empty or has insufficient columns."
    
    # Check for date column (first column)
    date_column = df.columns[0]
    try:
        df[date_column].apply(lambda x: pd.to_datetime(x, errors='coerce'))
    except:
        return False, f"First column ('{date_column}') must contain parseable dates."
    
    # Check for App 1 requirements (at least one numeric column for 'y')
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return False, "File must contain at least one numeric column for forecasting."
    
    # Check for App 2 and App 3 requirements
    expected_columns = [
        "Net sales/income from operations", "Total income from operations", "Employees cost",
        "depreciat", "Other expenses", "P/l before other inc. , int., excpt. items & tax",
        "Other income", "P/l before int., excpt. items & tax", "Interest",
        "P/l before exceptional items & tax", "Exceptional items", "P/l before tax",
        "Tax", "P/l after tax from ordinary activities", "Net profit/(loss) for the period",
        "Equity share capital", "Basic eps", "Diluted eps"
    ]
    if not any(col in df.columns for col in expected_columns):
        return False, "No expected financial columns found (e.g., 'Net sales/income from operations')."
    
    # Specifically check for App 3 required columns
    required_cols = ["Net sales/income from operations", "Net profit/(loss) for the period"]
    if not all(col in df.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        return False, f"Excel file must contain {', '.join(missing)} for revenue and profit analysis."
    
    return True, None

# Function for App 1: Financial Forecasting Dashboard
def app1(uploaded_file):
    st.header("Financial Forecasting")
    
    # Sidebar for model selection
    st.sidebar.header("Forecasting Model Selection")
    model_choice = st.sidebar.selectbox("Choose Model", ["Hybrid", "SARIMA"], key="app1_model_choice")

    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            # Validate file
            is_valid, error = validate_file(df)
            if not is_valid:
                st.error(error)
                return
            
            # Load and preprocess data based on model
            if model_choice == "Hybrid":
                processed_df, error = load_data_hybrid(df)
            else:  # SARIMA
                processed_df, error = load_data_sarima(df)
            
            if error:
                st.error(error)
            else:
                st.success("File successfully loaded and processed for forecasting!")
                
                # Run selected model
                with st.spinner(f"Running {model_choice} forecasting model..."):
                    if model_choice == "Hybrid":
                        results = run_hybrid_model(processed_df)
                    else:  # SARIMA
                        results = run_sarima_model(processed_df)
                
                # Extract results
                train_df = results["train_df"]
                test_df = results["test_df"]
                future_df = results["future_df"]
                metrics = results["metrics"]
                
                # Rename SARIMA prediction column to match Hybrid
                if model_choice == "SARIMA":
                    train_df = train_df.rename(columns={"sarima_pred": "final_pred"})
                    test_df = test_df.rename(columns={"sarima_pred": "final_pred"})
                
                # Display metrics (excluding R²)
                st.subheader("Model Performance Metrics")
                col1, col2, col3 = st.columns(3)
                col1.metric("MAE", f"{metrics['mae']:.2f}")
                col2.metric("RMSE", f"{metrics['rmse']:.2f}")
                col3.metric("MAPE", f"{metrics['mape']:.2f}%")
                
                # Plotting the forecast
                st.subheader("Forecasted Net Profit/(Loss)")
                fig = go.Figure()
                
                # Plot training data
                fig.add_trace(go.Scatter(
                    x=train_df["ds"], y=train_df["y"],
                    mode="lines+markers", name="Training Actual",
                    line=dict(color="blue")
                ))
                fig.add_trace(go.Scatter(
                    x=train_df["ds"], y=train_df["final_pred"],
                    mode="lines", name="Training Predicted",
                    line=dict(color="cyan", dash="dash")
                ))
                
                # Plot test data
                fig.add_trace(go.Scatter(
                    x=test_df["ds"], y=test_df["y"],
                    mode="lines+markers", name="Test Actual",
                    line=dict(color="green")
                ))
                fig.add_trace(go.Scatter(
                    x=test_df["ds"], y=test_df["final_pred"],
                    mode="lines", name="Test Predicted",
                    line=dict(color="lime", dash="dash")
                ))
                
                # Plot future forecast
                fig.add_trace(go.Scatter(
                    x=future_df["ds"], y=future_df["yhat"],
                    mode="lines+markers", name="Forecast",
                    line=dict(color="red")
                ))
                # Confidence interval
                fig.add_trace(go.Scatter(
                    x=future_df["ds"], y=future_df["yhat_upper"],
                    mode="lines", name="Upper Confidence",
                    line=dict(color="red", width=0),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=future_df["ds"], y=future_df["yhat_lower"],
                    mode="lines", name="Lower Confidence",
                    line=dict(color="red", width=0),
                    fill="tonexty", fillcolor="rgba(255, 0, 0, 0.1)",
                    showlegend=False
                ))
                
                # Customize plot
                fig.update_layout(
                    title="Hybrid Model Forecast" if model_choice == "Hybrid" else "SARIMA Model Forecast",
                    xaxis_title="Date",
                    yaxis_title="Net Profit/(Loss)(Cr)",
                    legend_title="Data",
                    showlegend=True
                )
                
                # Display plot
                st.plotly_chart(fig, use_container_width=True)
                
                # Display forecast table
                st.subheader("Forecasted Values")
                future_df_display = future_df[["ds", "yhat"]].copy()
                future_df_display["ds"] = future_df_display["ds"].dt.strftime("%Y-%m-%d")
                future_df_display = future_df_display.rename(columns={"ds": "Date", "yhat": "Forecasted Net Profit/(Loss)"})
                future_df_display["Forecasted Net Profit/(Loss)"] = future_df_display["Forecasted Net Profit/(Loss)"].round(2)
                st.dataframe(future_df_display, use_container_width=True)
                
                # Download forecast data
                csv = future_df_display.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="forecast.csv">Download Forecast CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"An error occurred in forecasting: {str(e)}")
    else:
        st.info("Please upload an Excel file to start forecasting.")

# Function for App 2: Dynamic Financial Insights Dashboard
def app2(uploaded_file):
    # Function to load and preprocess data
    @st.cache_data
    def load_data(uploaded_file):
        try:
            df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
            return None
        
        if df.empty or len(df.columns) < 2:
            st.error("Excel file is empty or has insufficient columns. Ensure it has a date column (first column) and financial data.")
            return None
        
        # Dynamically use the first column as the date column
        date_column = df.columns[0]
        
        # Define expected financial columns
        expected_columns = {
            "Net sales/income from operations": "net_sales",
            "Total income from operations": "total_income",
            "Employees cost": "employee_cost",
            "depreciat": "depreciation",
            "Other expenses": "other_expenses",
            "P/l before other inc. , int., excpt. items & tax": "op_profit",
            "Other income": "other_income",
            "P/l before int., excpt. items & tax": "pbit",
            "Interest": "interest",
            "P/l before exceptional items & tax": "pbet",
            "Exceptional items": "exceptional_items",
            "P/l before tax": "pbt",
            "Tax": "tax",
            "P/l after tax from ordinary activities": "pat_ordinary",
            "Net profit/(loss) for the period": "net_profit",
            "Equity share capital": "equity_capital",
            "Basic eps": "basic_eps",
            "Diluted eps": "diluted_eps"
        }
        
        # Validate financial columns
        existing_columns = {k: v for k, v in expected_columns.items() if k in df.columns}
        if not existing_columns:
            st.error("No expected financial columns found. Ensure the file has columns like 'Net sales/income from operations', 'depreciat', etc.")
            return None
        
        # Rename columns (date column to 'ds', others per expected_columns)
        rename_dict = {date_column: "ds", **existing_columns}
        df.rename(columns=rename_dict, inplace=True)
        
        # Parse dates and extract quarter
        def parse_quarter(date_str):
            month_map = {
                "Mar": ("03", "31", "Q1"), "Jun": ("06", "30", "Q2"),
                "Sep": ("09", "30", "Q3"), "Dec": ("12", "31", "Q4")
            }
            parts = str(date_str).split()
            if len(parts) < 2:
                return pd.NaT, None
            month = parts[0]
            year_suffix = parts[1]
            try:
                year = "20" + year_suffix if int(year_suffix) <= 50 else "19" + year_suffix
                month_num, day, quarter = month_map[month]
                date = pd.to_datetime(f"{year}-{month_num}-{day}")
                quarter_label = f"{quarter} {year}"
                return date, quarter_label
            except:
                return pd.NaT, None
        
        # Apply parsing and create columns
        df[["ds", "quarter"]] = df["ds"].apply(parse_quarter).apply(pd.Series)
        if df["ds"].isna().all():
            st.error(f"Failed to parse dates in the first column ('{date_column}'). Ensure format is like 'Mar 05 Q4'.")
            return None
        df = df.dropna(subset=["ds"]).sort_values("ds")
        
        return df

    # Function to calculate KPIs
    def calculate_kpis(df):
        kpis = {}
        
        # Revenue Growth
        if "net_sales" in df.columns:
            kpis["revenue_growth"] = df["net_sales"].ffill().pct_change(fill_method=None) * 100
        else:
            kpis["revenue_growth"] = np.nan
        
        # Operating Profit Margin
        if "op_profit" in df.columns and "net_sales" in df.columns:
            kpis["op_profit_margin"] = (df["op_profit"] / df["net_sales"]) * 100
        else:
            kpis["op_profit_margin"] = np.nan
        
        # Net Profit Margin
        if "net_profit" in df.columns and "net_sales" in df.columns:
            kpis["net_profit_margin"] = (df["net_profit"] / df["net_sales"]) * 100
        else:
            kpis["net_profit_margin"] = np.nan
        
        # Employee Cost Ratio
        if "employee_cost" in df.columns and "net_sales" in df.columns:
            kpis["employee_cost_ratio"] = (df["employee_cost"] / df["net_sales"]) * 100
        else:
            kpis["employee_cost_ratio"] = np.nan
        
        # Other Expenses Ratio
        if "other_expenses" in df.columns and "net_sales" in df.columns:
            kpis["other_expenses_ratio"] = (df["other_expenses"] / df["net_sales"]) * 100
        else:
            kpis["other_expenses_ratio"] = np.nan
        
        # Interest Coverage
        if "pbit" in df.columns and "interest" in df.columns:
            kpis["interest_coverage"] = df["pbit"] / df["interest"].replace(0, np.nan)
        else:
            kpis["interest_coverage"] = np.nan
        
        # Tax Rate
        if "tax" in df.columns and "pbt" in df.columns:
            kpis["tax_rate"] = (df["tax"] / df["pbt"].replace(0, np.nan)) * 100
        else:
            kpis["tax_rate"] = np.nan
        
        # Return on Equity
        if "net_profit" in df.columns and "equity_capital" in df.columns:
            kpis["roe"] = (df["net_profit"] / df["equity_capital"].replace(0, np.nan)) * 100
        else:
            kpis["roe"] = np.nan
        
        # Exceptional Items Impact
        if "exceptional_items" in df.columns and "pbet" in df.columns:
            kpis["exceptional_items_impact"] = (df["exceptional_items"] / df["pbet"].replace(0, np.nan)) * 100
        else:
            kpis["exceptional_items_impact"] = np.nan
        
        # Depreciation Ratio
        if "depreciation" in df.columns and "net_sales" in df.columns:
            kpis["depreciation_ratio"] = (df["depreciation"] / df["net_sales"]) * 100
        else:
            kpis["depreciation_ratio"] = np.nan
        
        # Assign KPIs to DataFrame
        for kpi, values in kpis.items():
            df[kpi] = values
        
        # Fill missing KPI values
        df = df.replace([np.inf, -np.inf], np.nan).ffill().bfill()
        
        return df

    # Function to generate hardcoded insights and suggestions (reverted to previous version)
    def generate_insights(df):
        insights = []
        suggestions = []
        
        # Get the latest and previous quarters
        latest_quarter = df.iloc[-1]
        prev_quarter = df.iloc[-2] if len(df) >= 2 else None
        prev_year_quarter = df[df["ds"] == latest_quarter["ds"] - pd.Timedelta(days=365)].iloc[0] if not df[df["ds"] == latest_quarter["ds"] - pd.Timedelta(days=365)].empty else None
        
        # 1. Profitability
        if "net_profit_margin" in df.columns:
            last_npm = latest_quarter["net_profit_margin"]
            prev_npm = prev_quarter["net_profit_margin"] if prev_quarter is not None else np.nan
            trend_npm = "increasing" if prev_quarter is not None and last_npm > prev_npm else "decreasing" if prev_quarter is not None else "stable"
            insights.append(f"Net Profit Margin: {last_npm:.2f}% in {latest_quarter['ds'].strftime('%b %Y')} ({trend_npm} from {prev_npm:.2f}% last quarter)")
            
            if trend_npm == "increasing":
                suggestions.append("**Maintain Profitability**: Continue strategies driving margin growth, such as high-margin services (e.g., AI, cloud).")
            elif trend_npm == "decreasing":
                suggestions.append("**Boost Revenue**: Explore new markets or subscription-based services to improve margins.")
                suggestions.append("**Cost Optimization**: Review operating expenses, focusing on employee costs and other expenses.")
        
        # 2. Cost Efficiency
        if "employee_cost_ratio" in df.columns:
            last_ecr = latest_quarter["employee_cost_ratio"]
            prev_ecr = prev_quarter["employee_cost_ratio"] if prev_quarter is not None else np.nan
            if last_ecr > 50:
                insights.append(f"Employee Cost Ratio: High at {last_ecr:.2f}% in {latest_quarter['ds'].strftime('%b %Y')}, compared to {prev_ecr:.2f}% last quarter.")
                suggestions.append("**Workforce Optimization**: Use freelancers or automation to reduce fixed employee costs.")
        
        if "other_expenses_ratio" in df.columns:
            last_oer = latest_quarter["other_expenses_ratio"]
            prev_oer = prev_quarter["other_expenses_ratio"] if prev_quarter is not None else np.nan
            if last_oer > 20:
                insights.append(f"Other Expenses Ratio: High at {last_oer:.2f}% in {latest_quarter['ds'].strftime('%b %Y')}, compared to {prev_oer:.2f}% last quarter.")
                suggestions.append("**Vendor Negotiation**: Renegotiate supplier contracts to lower other expenses.")
        
        # 3. Financial Stability
        if "interest_coverage" in df.columns:
            last_ic = latest_quarter["interest_coverage"]
            prev_ic = prev_quarter["interest_coverage"] if prev_quarter is not None else np.nan
            if last_ic < 3:
                insights.append(f"Interest Coverage Ratio: Low at {last_ic:.2f} in {latest_quarter['ds'].strftime('%b %Y')}, compared to {prev_ic:.2f} last quarter.")
                suggestions.append("**Debt Management**: Refinance high-interest debt to improve interest coverage.")
        
        # 4. Shareholder Value
        if "roe" in df.columns:
            last_roe = latest_quarter["roe"]
            prev_roe = prev_quarter["roe"] if prev_quarter is not None else np.nan
            trend_roe = "increasing" if prev_quarter is not None and last_roe > prev_roe else "decreasing" if prev_quarter is not None else "stable"
            insights.append(f"ROE: {last_roe:.2f}% in {latest_quarter['ds'].strftime('%b %Y')} ({trend_roe} from {prev_roe:.2f}% last quarter)")
            if trend_roe == "increasing":
                suggestions.append("**Enhance Shareholder Value**: Consider share buybacks or increased dividends to reward investors.")
        
        # 5. Tax Efficiency
        if "tax_rate" in df.columns:
            last_tr = latest_quarter["tax_rate"]
            prev_tr = prev_quarter["tax_rate"] if prev_quarter is not None else np.nan
            if last_tr > 25:
                insights.append(f"Tax Rate: High at {last_tr:.2f}% in {latest_quarter['ds'].strftime('%b %Y')}, compared to {prev_tr:.2f}% last quarter.")
                suggestions.append("**Tax Optimization**: Explore R&D tax credits or tax-efficient jurisdictions.")
        
        # 6. Year-over-Year Comparison
        if prev_year_quarter is not None and "net_profit_margin" in df.columns:
            yoy_npm = prev_year_quarter["net_profit_margin"]
            yoy_trend = "improved" if last_npm > yoy_npm else "declined"
            insights.append(f"Year-over-Year Net Profit Margin: {last_npm:.2f}% in {latest_quarter['ds'].strftime('%b %Y')} ({yoy_trend} from {yoy_npm:.2f}% in {prev_year_quarter['ds'].strftime('%b %Y')})")
            if yoy_trend == "declined":
                suggestions.append("**Strategic Review**: Analyze factors causing the year-over-year decline in profitability and address them.")
        
        return insights, suggestions

    # Function to generate LLM-based insights and suggestions
    def generate_llm_insights(df):
        try:
            # Get the latest and previous quarters
            latest_quarter = df.iloc[-1]
            prev_quarter = df.iloc[-2] if len(df) >= 2 else None
            latest_quarter_label = latest_quarter["quarter"]
            latest_year = int(latest_quarter_label.split()[-1])
            latest_q = latest_quarter_label.split()[0]
            prev_year_quarter_label = f"{latest_q} {latest_year - 1}"
            prev_year_quarter = df[df["quarter"] == prev_year_quarter_label].iloc[0] if prev_year_quarter_label in df["quarter"].values else None
            
            # Prepare KPI data
            kpi_data = {
                "latest_quarter_date": latest_quarter["ds"].strftime("%b %Y") if not pd.isna(latest_quarter["ds"]) else "Unknown",
                "latest_npm": latest_quarter.get("net_profit_margin", np.nan),
                "latest_opm": latest_quarter.get("op_profit_margin", np.nan),
                "latest_ecr": latest_quarter.get("employee_cost_ratio", np.nan),
                "latest_oer": latest_quarter.get("other_expenses_ratio", np.nan),
                "latest_ic": latest_quarter.get("interest_coverage", np.nan),
                "latest_tr": latest_quarter.get("tax_rate", np.nan),
                "latest_roe": latest_quarter.get("roe", np.nan),
                "latest_eii": latest_quarter.get("exceptional_items_impact", np.nan),
                "latest_dr": latest_quarter.get("depreciation_ratio", np.nan),
                "prev_quarter_date": prev_quarter["ds"].strftime("%b %Y") if prev_quarter is not None and not pd.isna(prev_quarter["ds"]) else "Unknown",
                "prev_npm": prev_quarter.get("net_profit_margin", np.nan) if prev_quarter is not None else np.nan,
                "prev_opm": prev_quarter.get("op_profit_margin", np.nan) if prev_quarter is not None else np.nan,
                "prev_ecr": prev_quarter.get("employee_cost_ratio", np.nan) if prev_quarter is not None else np.nan,
                "prev_oer": prev_quarter.get("other_expenses_ratio", np.nan) if prev_quarter is not None else np.nan,
                "prev_ic": prev_quarter.get("interest_coverage", np.nan) if prev_quarter is not None else np.nan,
                "prev_tr": prev_quarter.get("tax_rate", np.nan) if prev_quarter is not None else np.nan,
                "prev_roe": prev_quarter.get("roe", np.nan) if prev_quarter is not None else np.nan,
                "prev_eii": prev_quarter.get("exceptional_items_impact", np.nan) if prev_quarter is not None else np.nan,
                "prev_dr": prev_quarter.get("depreciation_ratio", np.nan) if prev_quarter is not None else np.nan,
                "prev_year_quarter_date": prev_year_quarter["ds"].strftime("%b %Y") if prev_year_quarter is not None and not pd.isna(prev_year_quarter["ds"]) else "Unknown",
                "yoy_npm": prev_year_quarter.get("net_profit_margin", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_opm": prev_year_quarter.get("op_profit_margin", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_ecr": prev_year_quarter.get("employee_cost_ratio", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_oer": prev_year_quarter.get("other_expenses_ratio", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_ic": prev_year_quarter.get("interest_coverage", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_tr": prev_year_quarter.get("tax_rate", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_roe": prev_year_quarter.get("roe", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_eii": prev_year_quarter.get("exceptional_items_impact", np.nan) if prev_year_quarter is not None else np.nan,
                "yoy_dr": prev_year_quarter.get("depreciation_ratio", np.nan) if prev_year_quarter is not None else np.nan,
            }
            
            # Format the prompt
            prompt = """
            You are a financial analysis expert tasked with generating dynamic insights and actionable suggestions based on quarterly financial data from a company's Excel file. The data includes key financial metrics and calculated KPIs, covering the latest quarter, the previous quarter, and the same quarter from the previous year (year-over-year comparison). Your goal is to analyze the provided data, identify trends, highlight significant changes, and provide strategic suggestions to improve financial performance.

            ### Input Data
            Below is the financial data for analysis:

            #### Latest Quarter (Date: {latest_quarter_date})
            - Net Profit Margin: {latest_npm:.2f}% (Net profit as a percentage of net sales)
            - Operating Profit Margin: {latest_opm:.2f}% (Operating profit as a percentage of net sales)
            - Employee Cost Ratio: {latest_ecr:.2f}% (Employee costs as a percentage of net sales)
            - Other Expenses Ratio: {latest_oer:.2f}% (Other expenses as a percentage of net sales)
            - Interest Coverage Ratio: {latest_ic:.2f} (Profit before interest and tax divided by interest expense)
            - Tax Rate: {latest_tr:.2f}% (Tax as a percentage of profit before tax)
            - Return on Equity (ROE): {latest_roe:.2f}% (Net profit as a percentage of equity capital)
            - Exceptional Items Impact: {latest_eii:.2f}% (Exceptional items as a percentage of profit before exceptional items and tax)
            - Depreciation Ratio: {latest_dr:.2f}% (Depreciation as a percentage of net sales)

            #### Previous Quarter (Date: {prev_quarter_date})
            - Net Profit Margin: {prev_npm:.2f}%
            - Operating Profit Margin: {prev_opm:.2f}%
            - Employee Cost Ratio: {prev_ecr:.2f}%
            - Other Expenses Ratio: {prev_oer:.2f}%
            - Interest Coverage Ratio: {prev_ic:.2f}
            - Tax Rate: {prev_tr:.2f}%
            - Return on Equity (ROE): {prev_roe:.2f}%
            - Exceptional Items Impact: {prev_eii:.2f}%
            - Depreciation Ratio: {prev_dr:.2f}

            #### Same Quarter Last Year (Date: {prev_year_quarter_date})
            - Net Profit Margin: {yoy_npm:.2f}%
            - Operating Profit Margin: {yoy_opm:.2f}%
            - Employee Cost Ratio: {yoy_ecr:.2f}%
            - Other Expenses Ratio: {yoy_oer:.2f}%
            - Interest Coverage Ratio: {yoy_ic:.2f}
            - Tax Rate: {yoy_tr:.2f}%
            - Return on Equity (ROE): {yoy_roe:.2f}%
            - Exceptional Items Impact: {yoy_eii:.2f}%
            - Depreciation Ratio: {yoy_dr:.2f}

            ### Instructions
            1. **Generate Insights**:
               - Analyze the provided KPIs to identify trends (increasing, decreasing, or stable) between the latest quarter and the previous quarter.
               - Compare the latest quarter's KPIs with the same quarter from the previous year to highlight year-over-year improvements or declines. If year-over-year data is unavailable (NaN or Unknown date), note it explicitly for that KPI.
               - Highlight any KPIs that are concerning based on the following thresholds:
                 - Net Profit Margin: Declining or below industry norms (e.g., <5% is concerning).
                 - Employee Cost Ratio: High if >50%.
                 - Other Expenses Ratio: High if >20%.
                 - Interest Coverage Ratio: Low if <3 (indicating potential debt servicing issues).
                 - Tax Rate: High if >25%.
                 - ROE: Declining or below industry norms (e.g., <10% is concerning).
                 - Exceptional Items Impact: Significant if >10% (indicating volatility).
               - Format each insight as a concise bullet point, including the KPI value, date, and trend (e.g., "Net Profit Margin: 8.5% in Mar 2025 (increasing from 7.2% last quarter)").
               - Include at least 4-6 insights, prioritizing profitability, cost efficiency, financial stability, and year-over-year performance.

            2. **Generate Suggestions**:
               - Based on the insights, provide actionable, strategic suggestions to improve financial performance.
               - Suggestions should address concerning KPIs or capitalize on positive trends. Examples:
                 - For declining Net Profit Margin: "Explore new revenue streams, such as subscription-based services, or optimize operating expenses."
                 - For high Employee Cost Ratio: "Consider automation or outsourcing to reduce fixed labor costs."
                 - For low Interest Coverage: "Refinance high-interest debt to lower interest expenses."
                 - For increasing ROE: "Consider share buybacks or dividend increases to enhance shareholder value."
                 - For high Tax Rate: "Investigate tax credits (e.g., R&D credits) or tax-efficient jurisdictions."
               - Format each suggestion as a bullet point with a clear action (e.g., "**Cost Optimization**: Review vendor contracts to reduce other expenses.").
               - Provide 4-6 suggestions, tailored to the insights and aligned with business strategies like cost management, revenue growth, or debt optimization.

            3. **Output Format**:
               - Return the response in the following structure:
                 ```
                 **Insights**:
                 - [Insight 1]
                 - [Insight 2]
                 - ...
                 **Suggestions**:
                 - [Suggestion 1]
                 - [Suggestion 2]
                 - ...
                 ```

            4. **Constraints**:
               - If a KPI value is missing (NaN or not provided), skip it in the analysis but note it in one insight (e.g., "Net Profit Margin data is unavailable for analysis.").
               - Ensure insights and suggestions are specific, avoiding vague recommendations like "improve performance."
               - Use the provided dates in a readable format (e.g., "Mar 2025").
               - Assume the company operates in a competitive industry (e.g., technology or manufacturing) unless specified otherwise.

            ### Example Output
            **Insights**:
            - Net Profit Margin: 8.5% in Mar 2025 (increasing from 7.2% in Dec 2024)
            - Employee Cost Ratio: 55% in Mar 2025 (high and increasing from 50% in Dec 2024)
            - Interest Coverage Ratio: 2.5 in Mar 2025 (low, decreasing from 3.2 in Dec 2024)
            - Year-over-Year Net Profit Margin: 8.5% in Mar 2025 (improved from 6.5% in Mar 2024)
            - ROE: 12% in Mar 2025 (stable from 11.8% in Dec 2024)
            **Suggestions**:
            - **Revenue Growth**: Launch new high-margin services to sustain net profit margin growth.
            - **Workforce Optimization**: Implement automation to reduce the high employee cost ratio.
            - **Debt Management**: Refinance debt to improve the low interest coverage ratio.
            - **Shareholder Value**: Consider dividend increases to leverage stable ROE.

            Now, analyze the provided data and generate insights and suggestions following the instructions above.
            """
            
            # Format the prompt with KPI data
            formatted_prompt = prompt.format(**kpi_data)
            
            # Call Gemini LLM
            response = gemini_model.generate_content(formatted_prompt)
            response_text = response.text.strip()
            
            # Parse the response
            insights = []
            suggestions = []
            current_section = None
            for line in response_text.split("\n"):
                line = line.strip()
                if line.startswith("**Insights**:"):
                    current_section = "insights"
                elif line.startswith("**Suggestions**:"):
                    current_section = "suggestions"
                elif line.startswith("- ") and current_section == "insights":
                    insights.append(line[2:])
                elif line.startswith("- ") and current_section == "suggestions":
                    suggestions.append(line[2:])
            
            return insights, suggestions
        
        except Exception as e:
            st.error(f"Failed to generate LLM insights: {str(e)}. Falling back to hardcoded insights.")
            return generate_insights(df)

    st.header("Financial Insights")
    st.write("""
        Analyze financial KPIs and get tailored suggestions based on historical data.
    """)
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is None:
            st.warning("Please upload a valid Excel file to proceed with insights.")
            return
        
        # Calculate KPIs
        df = calculate_kpis(df)
        
        # Sidebar for KPI selection
        st.sidebar.header("Insights Filter Options")
        kpis = [
            "revenue_growth", "op_profit_margin", "net_profit_margin",
            "employee_cost_ratio", "other_expenses_ratio", "interest_coverage",
            "tax_rate", "roe", "exceptional_items_impact", "depreciation_ratio"
        ]
        
        # Only include KPIs that have non-NaN values
        available_kpis = [kpi for kpi in kpis if not df[kpi].isna().all()]
        selected_kpis = st.sidebar.multiselect(
            "Select KPIs to Display",
            available_kpis,
            default=["net_profit_margin", "op_profit_margin"] if "net_profit_margin" in available_kpis else available_kpis[:2],
            key="app2_kpi_select"
        )
        
        # Plot selected KPIs
        st.subheader("KPI Trends")
        fig = go.Figure()
        for kpi in selected_kpis:
            fig.add_trace(go.Scatter(
                x=df["ds"], y=df[kpi], mode="lines", name=kpi.replace("_", " ").title()
            ))
        fig.update_layout(title="KPI Trends", xaxis_title="Date", yaxis_title="Value (%)", legend_title="KPIs")
        st.plotly_chart(fig, use_container_width=True)
        
        # Generate and display insights
        st.subheader("Dynamic Insights and Suggestions")
        use_llm = st.toggle("Use LLM for Insights", value=False, key="use_llm_toggle")
        
        if use_llm:
            if 'gemini_model' in globals():
                insights, suggestions = generate_llm_insights(df)
            else:
                st.error("Gemini API not configured. Falling back to hardcoded insights.")
                insights, suggestions = generate_insights(df)
        else:
            insights, suggestions = generate_insights(df)
        
        st.write("**Insights**:")
        for insight in insights:
            st.write(f"- {insight}")
        
        st.write("**Suggestions**:")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")
        
        # Display recent KPI values
        st.subheader("Recent KPIs (Last 4 Quarters)")
        st.dataframe(df.tail(4)[["ds", "quarter"] + selected_kpis].round(2))
        
        # Download insights as report
        report = "\n".join(["Dynamic Financial Insights Report", "\nInsights:"] + [f"- {i}" for i in insights] +
                           ["\nSuggestions:"] + [f"- {s}" for s in suggestions])
        st.download_button("Download Insights Report", report, file_name="financial_insights_report.txt", key="app2_download")
    else:
        st.info("Please upload an Excel file to view insights.")

# Main app
def main():
    st.title("ARK Financial Dashboards")
    st.write("Upload an Excel file to perform financial forecasting, analyze KPIs, and visualize financial metric changes.")
    
    # Display logo at the top of the sidebar
    st.sidebar.image(r"C:\Users\Aditya\Desktop\FyPro\Companies\Dashboard\Logo.svg", width=150)
    
    # Single file uploader
    uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"], key="shared_file_uploader")
    
    # Run App 1
    app1(uploaded_file)
    
    # Separator
    st.divider()
    
    # Run App 2
    app2(uploaded_file)
    
    # Separator
    st.divider()
    
    # Run App 3: Heatmap Dashboard
    st.sidebar.header("Heatmap Options")
    metric = st.sidebar.selectbox(
        "Select Metric",
        ["Total Revenue", "Net Profit"],
        key="app3_metric_select"
    )
    run_heatmap_dashboard(uploaded_file, metric)
    
    # Separator
    st.divider()
    
    # Run App 4: Financial Flow Sankey
    st.header("Financial Flow Sankey")
    run_sankey_diagram(uploaded_file)

if __name__ == "__main__":
    main()