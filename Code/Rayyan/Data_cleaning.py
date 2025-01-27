import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer

# Define reverse function
def reverse_columns_in_groups(df, start_index, group_size=5):
    """
    Reverses columns in groups of a specified size.

    Parameters:
    - df: The dataframe.
    - start_index: The starting index of the columns to reverse.
    - group_size: Number of columns in each group to reverse.
    
    Returns:
    - Updated dataframe with columns reversed in groups.
    """
    if start_index >= len(df.columns):
        raise ValueError("start_index is larger than the number of columns in the dataframe.")

    cols = df.columns[start_index:]
    reversed_cols = []

    for i in range(0, len(cols), group_size):
        group = cols[i:i + group_size]
        reversed_cols.extend(group[::-1])

    new_columns = list(df.columns[:start_index]) + reversed_cols
    return df[new_columns]

def handling_missing_values(df):
    # print(type(type_1))
    if df.iloc[0,1] == "12 mths":
        df.replace("12 mths",np.nan,inplace=True)

    result_0 = (df == "0.00").stack().idxmax()
    if result_0:
        df.replace("0.00",np.nan,inplace=True)
        print("First Occurance for '0.00 'is :- ",result_0)
    else:
        print("None occured in for '0.00' in df")

    result_ = (df == "--").stack().idxmax()
    if result_:
        print("First Occurance '--' is:- ",result_)
        df.replace("--",np.nan,inplace=True)
    else:
        print("None occurance for '--' in df")
        
    return df

def checking_dtype(df,pos_1,pos_2):
    type_1 = df.iloc[pos_1,pos_2]
    print(type_1)
    print(__builtins__.type(type_1))
    
def convert_dtr_float(df):      
    df.iloc[1:, 1:] = df.iloc[1:, 1:].replace({',': ''}, regex=True).astype(float)
    return df

def checking_for_missing_values(df):
    missing_value = df.isnull()
    missing_value.tail(20)

    print(missing_value.sum().sum())  # Prints total number of NaN values in the entire DataFrame
    df.tail(20)

    for index, row in df.iterrows():
        # Skip the first column (financial term) and check for NaN values in the rest of the row
        nan_count = row[1:].isnull().sum()  # Check for NaN from the second column onward
        total_length = len(row[1:])  # Get the total length of the row (excluding the first column)
        
        if nan_count > 0:
            print(f"Financial Term: {row[0]} - NaN values: {nan_count} out of {total_length} columns")
    
    for column in missing_value.columns.values.tolist():
        # print(column)
        print(missing_value[column].value_counts())
        print("")

def finding_null_values(df):
    # Assuming you already have a DataFrame (df) with your data
    high_null_values = []
    less_null_values = []

    # Iterate through each row (excluding the first column, which contains the row names)
    for index, row in df.iterrows():
        # Count the number of null values in the row (excluding the 0th column)
        null_count = row[1:].isnull().sum()

        # Check if the null count is greater than 10
        if null_count > 10:
            high_null_values.append(row[0])  # Add the row name (0th column) to high_null_values list
        # Check if the null count is greater than or equal to 1 but less than or equal to 10
        elif null_count >= 1 and null_count <= 10:
            less_null_values.append(row[0])  # Add the row name (0th column) to less_null_values list

    # Print the results
    print("Rows with more than 10 null values:", high_null_values)
    print("Rows with 1 to 10 null values:", less_null_values)
    print(len(high_null_values))
    print(len(less_null_values))
    print(len(df))
    
    return [high_null_values,less_null_values]


def cleaning_data(df,less_null_values,high_null_values,save_path_relative):
    if len(less_null_values) > 0:
        # Iterate through the DataFrame and delete rows with names in high_null_values
        df_cleaned = df[~df.iloc[:, 0].isin(high_null_values)]

        # Reset the row index after removing the rows
        df_cleaned = df_cleaned.reset_index(drop=True)
        df = df_cleaned
        df_cleaned.to_excel(save_path_relative, index=False)
        # Print the cleaned DataFrame
        print(df_cleaned)


        missing_value = df.isnull()
        missing_value.tail(20)

        for column in missing_value.columns.values.tolist():
            # print(column)
            print(missing_value[column].value_counts())
            print("")

        df = df.T.reset_index()
        df.columns = ['Year'] + list(df.columns[1:])  # Rename the index column to "Year"
        df.to_excel(save_path_relative,index = False)

        df_columns = df.iloc[0,1:]

        print(less_null_values)


        # Set the first row as the header
        df.columns = df.iloc[0]  # Assign the first row as the column headers
        df = df[1:]  # Remove the first row since it's now the header

        # Reset the index (optional)
        df.reset_index(drop=True, inplace=True)


        # Check if all columns in less_null_values exist in the DataFrame
        missing_columns = [col for col in less_null_values if col not in df.columns]
        if missing_columns:
            print(f"Columns not found in DataFrame: {missing_columns}")
        else:
            # Convert columns to numeric (if not already numeric)
            df[less_null_values] = df[less_null_values].apply(pd.to_numeric, errors='coerce')

            # Initialize the SimpleImputer with the strategy set to 'mean'
            imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

            # Fit and transform the specified columns
            df[less_null_values] = imputer.fit_transform(df[less_null_values])

            # Print the updated DataFrame (optional)
            print(df)

            # Save the updated DataFrame to Excel (optional)
            df.to_excel(save_path_relative, index=False)

        print(df.head(5))
    else:
        df = df.dropna(axis=0)
        df = df.reset_index(drop=True)
        df = df.T.reset_index()
        df.columns = ['Year'] + list(df.columns[1:])
        df.to_excel(save_path_relative,index=False)

if __name__ == '__main__':    
    # Current working directory
    current_dir = os.getcwd()

    # File path construction
    site = "MoneyControl"
    sector = "IT Services & Consulting"
    company_name = "3i Infotech Ltd"
    file_name = "Profit-loss_combined.xlsx"
    file_name_2 = "Profit-loss_combined_2.xlsx"

    input_path_relative = os.path.join(current_dir, "Financial_Data", site, "Companies", sector, company_name, "Excel",file_name)
    print("Input file: ", input_path_relative)

    save_path_relative = os.path.join(current_dir, "Financial_Data", site, "Companies", sector, company_name, "Pruned_Excel",file_name_2)
    # Check if file exists
    if not os.path.exists(input_path_relative):
        raise FileNotFoundError(f"Input file does not exist: {input_path_relative}")
    
    
    # Load the Excel file
    try:
        df = pd.read_excel(input_path_relative)
        print(df.head())
    except Exception as e:
        print(f"Error reading the Excel file: {e}")

    # Start index where year columns begin
    start_index = 1  # Assuming the first column contains non-year data
    reversed_df = reverse_columns_in_groups(df, start_index=start_index)

    df = reversed_df
    print(df.head(5))

    df = handling_missing_values(df)
    df.to_excel(save_path_relative,index=False)

    checking_dtype(df,6,5)

    df = convert_dtr_float(df)

    checking_dtype(df,6,5)

    checking_for_missing_values(df)

    df.to_excel(save_path_relative,index=False)

    high_null_values = finding_null_values(df)[0]
    less_null_values = finding_null_values(df)[1]

    print(high_null_values)
    print(less_null_values)

    cleaning_data(df,less_null_values,high_null_values,save_path_relative)