import sqlite3

DB_NAME = "backend/lineage.db"


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