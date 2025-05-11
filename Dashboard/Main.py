import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
import base64
import os
from dotenv import load_dotenv
import google.generativeai as genai
from HybridF import load_data as load_data_hybrid, run_hybrid_model
from SarimaF import load_data as load_data_sarima, run_sarima_model
from Heatmap import run_heatmap_dashboard
from SankeyF import run_sankey_diagram
from Function.app1 import app1
from Function.app2 import app2
# Load environment variables from .env file
load_dotenv()
current_dic = os.getcwd()
# Streamlit app configuration
st.set_page_config(page_title="ARK Financial Dashboards", layout="wide")

# Configure Gemini API
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.warning(f"Failed to configure Gemini API: {str(e)}. LLM insights will not be available.")


# Main app
def main():
    st.title("ARK Financial Dashboards")
    st.write("Upload an Excel file to perform financial forecasting, analyze KPIs, and visualize financial metric changes.")
    
    # Display logo at the top of the sidebar
    st.sidebar.image(fr"{current_dic}/Dashboard/Logo.svg", width=150)
    
    # Single file uploader
    uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"], key="shared_file_uploader")
    
    # Run App 1
    app1(uploaded_file,st,pd,go,np,base64,load_data_hybrid,load_data_sarima,run_hybrid_model,run_sarima_model)
    
    # Separator
    st.divider()
    
    # Run App 2
    app2(uploaded_file,st,pd,np,gemini_model,go)
    
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