
# Function to validate the uploaded file
def validate_file(df,pd,np):
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
def app1(uploaded_file,st,pd,go,np,base64,load_data_hybrid,load_data_sarima,run_hybrid_model,run_sarima_model):
    st.header("Financial Forecasting")
    
    # Sidebar for model selection
    st.sidebar.header("Forecasting Model Selection")
    model_choice = st.sidebar.selectbox("Choose Model", ["Hybrid", "SARIMA"], key="app1_model_choice")

    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            # Validate file
            is_valid, error = validate_file(df,pd,np)
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