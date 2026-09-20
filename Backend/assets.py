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

'''if __name__ == "__main__":
    assets = get_all_assets()
    print("\n ASSETS REGISTRY \n")

    for asset in assets:
        print("Asset ID : ", asset[0])
        print("Name : ", asset[1])
        print("Type : ", asset[2])
        print("Owner : ", asset[3])
        print("Environment : ", asset[4])
        print("Criticality : ", asset[5])
        print("Lifecycle : ", asset[6])
        print("-" * 40)'''

if __name__ == "__main__":
    keyword = input("Enter asset name to search :")
    assets = search_assets(keyword)
    print("\n SEARCH RESULT \n")

    for asset in assets:
        print("Asset ID : ", asset[0])
        print("Name : ", asset[1])
        print("Type : ", asset[2])
        print("Owner : ", asset[3])
        print("Environment : ", asset[4])
        print("Criticality : ", asset[5])
        print("Lifecycle : ", asset[6])
        print("-" * 40)