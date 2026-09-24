import sqlite3

DB_NAME = "lineage.db"


def get_all_assets():
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM assets
    """)

    assets = cursor.fetchall()

    connection.close()

    return assets


def search_assets(keyword):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM assets
        WHERE asset_name LIKE ?
    """, ("%" + keyword + "%",))

    assets = cursor.fetchall()

    connection.close()

    return assets


def get_asset(asset_id):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM assets
        WHERE asset_id = ?
    """, (asset_id,))

    asset = cursor.fetchone()

    connection.close()

    return asset


# Test the registry
if __name__ == "__main__":

    assets = get_all_assets()

    print("\n===== ASSET REGISTRY =====")

    for asset in assets:
        print(asset)

    print("\nTotal assets:", len(assets))


#Test for search assets 

if __name__ == "__main__":

    keyword = input("Enter asset name to search: ")

    assets = search_assets(keyword)

    print("\n===== SEARCH RESULTS =====\n")

    for asset in assets:
        print("ID:", asset[0])
        print("Name:", asset[1])
        print("Type:", asset[2])
        print("Owner:", asset[3])
        print("Criticality:", asset[5])
        print("-" * 40)



# Filtering the asset type 

def get_assets_by_type(asset_type):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM assets
        WHERE asset_type = ?
    """, (asset_type,))

    assets = cursor.fetchall()

    connection.close()

    return assets



if __name__ == "__main__":

    asset_type = input("Enter asset type: ")

    assets = get_assets_by_type(asset_type)

    print("\n===== ASSETS =====\n")

    for asset in assets:
        print("ID:", asset[0])
        print("Name:", asset[1])
        print("Type:", asset[2])
        print("Owner:", asset[3])
        print("-" * 40)


# Function to create a new asset

def add_asset(asset_id, asset_name, asset_type, owner,
              environment, criticality, lifecycle):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT asset_id FROM assets WHERE asset_id = ?",
        (asset_id,)
    )

    existing_asset = cursor.fetchone()

    if existing_asset:
        print("Error: Asset ID already exists.")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO assets
        (asset_id, asset_name, asset_type, owner,
         environment, criticality, lifecycle)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        asset_id,
        asset_name,
        asset_type,
        owner,
        environment,
        criticality,
        lifecycle
    ))

    connection.commit()

    connection.close()

    print("Asset added successfully!")




if __name__ == "__main__":

    add_asset(
        "A016",
        "Marketing Database",
        "Database",
        "Marketing IT",
        "Production",
        "Medium",
        "Active"
    )



