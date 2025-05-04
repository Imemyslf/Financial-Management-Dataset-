import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
        return df
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        return None

def process_sankey_data(df, quarter, quarter_col):
    # Filter data for the selected quarter
    df_quarter = df[df[quarter_col] == quarter].copy()
    
    if df_quarter.empty:
        st.error(f"No data available for quarter {quarter}")
        return None, None, None, None
    
    # Define input and output parameters
    input_params = ["Net sales/income from operations", "Other income"]
    output_params = ["Employees cost", "depreciat", "Other expenses", "Interest", 
                     "Tax", "Net profit/(loss) for the period"]
    
    # Validate required columns
    required_cols = input_params + output_params
    missing_cols = [col for col in required_cols if col not in df_quarter.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
        return None, None, None, None
    
    # Extract values for the quarter
    input_values = df_quarter[input_params].iloc[0].to_dict()
    output_values = df_quarter[output_params].iloc[0].to_dict()
    
    # Create nodes: inputs + breaker + outputs
    breaker_node = ["Revenue"]
    all_nodes = input_params + breaker_node + output_params
    node_labels = all_nodes
    node_colors = ['#1E90FF'] * len(input_params) + ['#32CD32'] + ['#FF4500'] * (len(output_params) - 1) + ['#32CD32']
    
    # Create node values for hover
    total_income = sum(input_values.values())
    node_values = [input_values.get(param, 0) for param in input_params] + [total_income] + [output_values.get(param, 0) for param in output_params]
    
    # Create links
    sources = []
    targets = []
    values = []
    link_colors = []
    
    if total_income == 0:
        st.error(f"Total income is zero for quarter {quarter}")
        return None, None, None, None
    
    # Links from inputs to breaker
    breaker_index = len(input_params)  # Index of Breaker node
    for i, input_node in enumerate(input_params):
        input_value = input_values[input_node]
        if input_value > 0:
            sources.append(i)
            targets.append(breaker_index)
            values.append(input_value)
            link_colors.append('rgba(30, 144, 255, 0.4)')  # Blue with transparency
    
    # Links from breaker to outputs
    for j, output_node in enumerate(output_params):
        output_value = output_values[output_node]
        if output_value > 0:
            sources.append(breaker_index)
            targets.append(breaker_index + 1 + j)  # Outputs start after breaker
            values.append(output_value)
            # Link color matches output node
            if output_node == "Net profit/(loss) for the period":
                link_colors.append('rgba(50, 205, 50, 0.4)')  # Green with transparency
            else:
                link_colors.append('rgba(255, 69, 0, 0.4)')  # Red with transparency
    
    return node_labels, node_colors, dict(source=sources, target=targets, value=values, color=link_colors), node_values

def create_sankey_diagram(node_labels, node_colors, links, node_values):
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=5,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors,
            customdata=node_values,
            hovertemplate='%{label}: %{customdata}<extra></extra>'
        ),
        link=links
    )])
    
    fig.update_layout(
        title_text="Financial Flow Sankey Diagram",
        font=dict(size=15, color="white"),
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        width=1000,
        height=600
    )
    
    return fig

def run_sankey_diagram(uploaded_file):
    st.write("Visualize the flow of financial resources from income sources to expenses and profit/loss for a selected quarter.")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            # Use the first column as the quarter column
            quarter_col = df.columns[0]
            quarters = df[quarter_col].unique().tolist()  # Preserve order from Excel file
            quarters = quarters[::-1]  # Reverse to put latest quarter at the top
            st.sidebar.header("Sankey Option")
            selected_quarter = st.sidebar.selectbox("Select Quarter", quarters, index=0)  # Default to first (latest) quarter
            
            # Process data and create Sankey diagram
            node_labels, node_colors, links, node_values = process_sankey_data(df, selected_quarter, quarter_col)
            
            if node_labels is not None:
                fig = create_sankey_diagram(node_labels, node_colors, links, node_values)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please upload an Excel file to generate the Sankey diagram.")