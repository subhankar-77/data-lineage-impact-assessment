import sqlite3
DB_NAME = "lineage.db"

def get_all_assets():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("Select * from assets")
    assets = cursor.fetchall()
    connection.close()
    return assets

def search_assets(keyword):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""Select * from assets where asset_name like ? """, ("%" + keyword + "%",))
    assets = cursor.fetchall()
    connection.close()
    return assets

def get_assets_by_type(asset_type):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""Select * from assets where asset_type = ? """, (asset_type,))
    assets = cursor.fetchall()
    connection.close()
    return assets

def add_asset(asset_id, asset_name, asset_type, owner, environment, criticality, lifecycle):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("Select asset_id from assets where asset_id = ?",(asset_id,))
    existing_asset = cursor.fetchone()
    if existing_asset:
        print("Error : Asset Id already exists")
        connection.close()
        return
    cursor.execute("""Insert into assets(asset_id, asset_name, asset_type, owner, environment, criticality, lifecycle) values (?, ?, ?, ?, ?, ?, ?)""",(asset_id, asset_name, asset_type, owner, environment, criticality, lifecycle))
    connection.commit()
    connection.close()
    print("Asset added successfully.")
        

# if __name__ == "__main__":
#     assets = get_all_assets()
#     print("\n ASSETS REGISTRY \n")

#     for asset in assets:
#         print("Asset ID : ", asset[0])
#         print("Name : ", asset[1])
#         print("Type : ", asset[2])
#         print("Owner : ", asset[3])
#         print("Environment : ", asset[4])
#         print("Criticality : ", asset[5])
#         print("Lifecycle : ", asset[6])
#         print("-" * 40)

# if __name__ == "__main__":
#     keyword = input("Enter asset name to search :")
#     assets = search_assets(keyword)
#     print("\n SEARCH RESULT \n")

    # for asset in assets:
    #     print("Asset ID : ", asset[0])
    #     print("Name : ", asset[1])
    #     print("Type : ", asset[2])
    #     print("Owner : ", asset[3])
    #     print("Environment : ", asset[4])
    #     print("Criticality : ", asset[5])
    #     print("Lifecycle : ", asset[6])
    #     print("-" * 40)

# if __name__ == "__main__":
#     asset_type = input("Enter asset type to search :")
#     assets = get_assets_by_type(asset_type)
#     print("\n  ASSETS \n")

#     for asset in assets:
#         print("Asset ID : ", asset[0])
#         print("Name : ", asset[1])
#         print("Type : ", asset[2])
#         print("Owner : ", asset[3])
#         print("Environment : ", asset[4])
#         print("Criticality : ", asset[5])
#         print("Lifecycle : ", asset[6])
#         print("-" * 40)

#if __name__ == "__main__":
 #   add_asset("A016","Marketing Database", "Database", "Marketing IT", "Production", "Medium", "Active")