from assets import get_all_assets, search_assets, get_assets_by_type

print("\n All ASSETS ")
assets = get_all_assets()
for asset in assets:
    print(asset)

print("\n CUSTOMER SEARCH ")
customer_assets = search_assets("Customer")
for asset in customer_assets:
    print(asset)

print("\n PIPELINES ")
pipelines = get_assets_by_type("Pipeline")
for asset in pipelines:
    print(asset)