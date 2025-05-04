import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def load_data_app3(uploaded_file, metric):
    # Load the data
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        return None
    
    if df.empty or len(df.columns) < 2:
        st.error("Excel file is empty or has insufficient columns.")
        return None
    
    # Ensure correct columns
    date_col = df.columns[0]
    
    # Map metric to column name
    metric_columns = {
        "Total Revenue": "Total Revenue",
        "Net Profit": "Net profit/(loss) for the period"
    }
    revenue_col = metric_columns.get(metric)
    if revenue_col not in df.columns:
        st.error(f"Required column '{revenue_col}' not found in the uploaded file.")
        return None
    
    # Handle custom date format like 'Mar 05 Q4'
    def extract_year_quarter(x):
        parts = str(x).split()
        if len(parts) >= 3:
            year_suffix = parts[1]
            quarter = int(parts[2][1])  # 'Q4' -> 4
            year = int('20' + year_suffix)  # '05' -> 2005
            return pd.Series([year, quarter])
        else:
            return pd.Series([np.nan, np.nan])

    df[['Year', 'Quarter']] = df[date_col].apply(extract_year_quarter)
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['Year', 'Quarter'])
    
    # Calculate % change quarter over quarter
    df['Revenue Change %'] = df[revenue_col].pct_change() * 100
    
    # Keep only last 3 years
    latest_year = df['Year'].max()
    years_to_include = [latest_year - i for i in range(3)]
    df_filtered = df[df['Year'].isin(years_to_include)]
    
    # Pivot the table: Rows -> Year, Columns -> Quarter
    heatmap_data = df_filtered.pivot(index='Year', columns='Quarter', values='Revenue Change %')
    
    # Reorder years so latest year is on top
    heatmap_data = heatmap_data.sort_index(ascending=False)
    
    # Ensure Q1-Q4 order for columns in calculation
    heatmap_data = heatmap_data[[1, 2, 3, 4]]
    
    return heatmap_data

def run_heatmap_dashboard(uploaded_file, metric):
    # Set container background and text color
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.header("QoQ Growth Heatmap")
    # st.write(f"Visualize percentage changes in {metric} over the last 3 years, compared to the previous quarter.")

    if uploaded_file is not None:
        # Load and process data
        heatmap_data = load_data_app3(uploaded_file, metric)
        
        if heatmap_data is not None:
            # Reorder columns for display: Q4, Q1, Q2, Q3
            display_data = heatmap_data[[4, 1, 2, 3]]
            
            # Plotting
            st.subheader(f"Percentage Change in {metric} (Last 3 Years)")
            # Add space between header and heatmap
            st.markdown("<div style='padding: 20px 0;'></div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 4))  # Reduced height from 6 to 4

            # Set background colors
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')

            # Create a dummy heatmap (just to set up the grid), without colorbar
            sns.heatmap(
                display_data, 
                annot=False, 
                fmt=".2f", 
                cmap='Greys', 
                cbar=False, 
                linewidths=0.5, 
                linecolor='grey',
                ax=ax
            )

            # Loop over data dimensions and create text annotations with custom colors
            for y in range(display_data.shape[0]):
                for x in range(display_data.shape[1]):
                    value = display_data.iloc[y, x]
                    if pd.isna(value):
                        text = ''
                        bg_color = '#0e1117'
                    else:
                        text = f"{value:.2f}%"
                        if value >= 0:
                            bg_color = '#171E10'  # Greenish background for increase
                            text_color = '#6EF009'  # Bright green text
                        else:
                            bg_color = '#1D1010'  # Reddish background for decrease
                            text_color = '#DB0101'  # Bright red text

                    # Set background color
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color=bg_color, ec='grey'))

                    # Add text
                    if text != '':
                        ax.text(x + 0.5, y + 0.5, text, 
                                ha='center', va='center', color=text_color, fontsize=12, fontweight='bold')

            # Set labels
            # ax.set_title(f'{metric}', fontsize=16, pad=20, color='white')
            ax.set_xlabel('')
            ax.set_ylabel('Year', fontsize=12, color='white')

            # Set ticks - columns on top, labeled to match reordered data
            ax.xaxis.tick_top()  # Move column labels to top
            ax.set_xticks([0.5, 1.5, 2.5, 3.5])
            ax.set_xticklabels(['Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec'], fontsize=12, color='white')

            ax.set_yticks(np.arange(len(display_data)) + 0.5)
            ax.set_yticklabels(display_data.index, fontsize=12, color='white')

            # Remove grid lines inside the cells
            ax.tick_params(axis='both', which='both', length=0, colors='white')

            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Unable to process the uploaded file for heatmap analysis.")
    else:
        st.info("Please upload an Excel file to generate the heatmap.")