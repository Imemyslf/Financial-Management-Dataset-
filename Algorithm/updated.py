import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import json
import seaborn as sns

# Load the JSON data
with open("../data/Reliance/QuarterlyExcel/list.json", "r") as f:
    jData = json.load(f)

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



