import pandas as pd


adani_Ports = pd.read_excel("./data/AdaniPorts/Excel/Adani_Ports_yearly.xlsx")
larsen_Toubro = pd.read_excel("./data/LarsenToubro/Excel/larsenToubro_yearly.xlsx")
reliance = pd.read_excel("./data/Reliance/Excel/reliance_yearly.xlsx")


adani_Ports.set_index(adani_Ports.columns[0], inplace=True)
larsen_Toubro.set_index(larsen_Toubro.columns[0], inplace=True)
reliance.set_index(reliance.columns[0], inplace=True)


common_parameters = adani_Ports.index.intersection(larsen_Toubro.index).intersection(reliance.index)


common_data = pd.DataFrame({
    "Parameters": common_parameters,
    "Adani Ports": adani_Ports.loc[common_parameters].iloc[:, 0],  
    "Larsen Toubro": larsen_Toubro.loc[common_parameters].iloc[:, 0],  
    "Reliance": reliance.loc[common_parameters].iloc[:, 0]  
})


common_data = common_data.dropna()


common_data.to_excel("../Filtered Excel/Filtered_yaerly.xlsx", index=False)

print("Filtered_yaerly.xlsx created successfully")
