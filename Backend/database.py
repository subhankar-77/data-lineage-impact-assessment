import sqlite3
import pandas as pd

# Database file
DB_NAME = "lineage.db"

# Connect to SQLite
connection = sqlite3.connect(DB_NAME)

# Read CSV files
assets = pd.read_csv("Data/assets.csv")
relationships = pd.read_csv("Data/relationships.csv")

# Store data in SQLite
assets.to_sql("assets", connection, if_exists="replace", index=False)
relationships.to_sql("relationships", connection, if_exists="replace", index=False)

print("Database created Successfully !")

#  Show number of records
print("Number of assets : ", len(assets))
print("Number of relationships : ", len(relationships))

# Close connection
connection.close()
