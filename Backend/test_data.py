import pandas as pd
assets =  pd.read_csv("Data/assets.csv")
relationships = pd.read_csv("Data/relationships.csv")

print("\nNumber of assets : ", len(assets))
print("\nNumber of relationships : ", len(relationships))

print("\nFirst 5 assets : ")
print(assets.head())

print("\nRelationships : ")
print(relationships)