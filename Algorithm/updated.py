# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# import json

# import seaborn as sns

# # Create a DataFrame


# # Load the JSON data
# with open("../data/Reliance/QuarterlyExcel/list.json", "r") as f:
#     jData = json.load(f)

# # Sample data: Replace this with your actual dataset
# data = {
#     'Quarter': ['Sep 14', 'Jun 14', 'Mar 14', 'Dec 13', 'Sep 13'],    
# }

# data_name = []
# for i, (row, value) in enumerate(jData.items()):
#     keyValue = row
#     data_name.append(row)
#     data[keyValue] = [float(x.replace(',', '')) if x != '--' else 0 for x in value]

# print("Data Name :- \n", data_name)

# pretty_data = json.dumps(data, indent=4)
# print("Data: \n", pretty_data)

# # Create a DataFrame
# df = pd.DataFrame(data)

# # Select the features for clustering (only numerical data)
# features = df[data_name]

# df = pd.DataFrame(data)

# # Create pair plots
# sns.pairplot(df[data_name])
# plt.title('Pair Plot of Financial Metrics')
# plt.show()

# # Standardize the features
# scaler = StandardScaler()
# scaled_features = scaler.fit_transform(features)

# # Apply K-Means Clustering
# kmeans = KMeans(n_clusters=3)  # You can adjust the number of clusters
# df['Cluster'] = kmeans.fit_predict(scaled_features)

# Visualizing the clusters
# plt.scatter(df['Net Sales/Income from operations '], df['Net Profit/(Loss) For the Period'], c=df['Cluster'], cmap='viridis')
# plt.title('K-Means Clustering of Reliance Industries Financial Data')
# plt.xlabel('Net Sales (in Rs. Cr)')
# plt.ylabel('Net Profit (in Rs. Cr)')
# plt.colorbar(label='Cluster')
# plt.show()

# Print the clustered data
# print(df)

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import json
import seaborn as sns

# Load the JSON data
with open("../data/Reliance/QuarterlyExcel/list.json", "r") as f:
    jData = json.load(f)

# Sample data: Replace this with your actual dataset
data = {
    'Quarter': ['Sep 14', 'Jun 14', 'Mar 14', 'Dec 13', 'Sep 13'],    
}

data_name = []
for row, value in jData.items():
    keyValue = row
    data_name.append(row)
    # Convert values to float, replacing '--' with 0
    data[keyValue] = [float(x.replace(',', '')) if x != '--' else 0 for x in value]

print("Data Name :- \n", data_name)

# Create a DataFrame
df = pd.DataFrame(data)

# Create pair plots
sns.pairplot(df[data_name])  # Ensure you're passing the DataFrame with numerical data
plt.suptitle('Pair Plot of Financial Metrics', y=1.02)  # Adjust the title position
plt.show()



