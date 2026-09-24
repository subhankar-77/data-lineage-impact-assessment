import csv
import os
import random
from datetime import date, timedelta


# ==================================================
# SETTINGS
# ==================================================

OUTPUT_DIR = "data"

ASSET_FILE = os.path.join(
    OUTPUT_DIR,
    "assets.csv"
)

RELATIONSHIP_FILE = os.path.join(
    OUTPUT_DIR,
    "relationships.csv"
)


random.seed(42)


# ==================================================
# BUSINESS DOMAINS
# ==================================================

domains = [
    "Customer",
    "Orders",
    "Employee",
    "Product",
    "Payment",
    "Inventory",
    "Marketing",
    "Logistics",
    "Supplier",
    "Finance"
]


# ==================================================
# DOMAIN CONFIGURATION
# ==================================================

domain_config = {

    "Customer": {
        "owner": "Customer Data Team",
        "department": "Customer",
        "criticality": "High"
    },

    "Orders": {
        "owner": "Order Data Team",
        "department": "Sales",
        "criticality": "High"
    },

    "Employee": {
        "owner": "HR Data Team",
        "department": "Human Resources",
        "criticality": "Medium"
    },

    "Product": {
        "owner": "Product Data Team",
        "department": "Product",
        "criticality": "High"
    },

    "Payment": {
        "owner": "Finance Data Team",
        "department": "Finance",
        "criticality": "High"
    },

    "Inventory": {
        "owner": "Inventory Data Team",
        "department": "Operations",
        "criticality": "High"
    },

    "Marketing": {
        "owner": "Marketing Data Team",
        "department": "Marketing",
        "criticality": "Medium"
    },

    "Logistics": {
        "owner": "Logistics Data Team",
        "department": "Operations",
        "criticality": "High"
    },

    "Supplier": {
        "owner": "Supplier Data Team",
        "department": "Procurement",
        "criticality": "Medium"
    },

    "Finance": {
        "owner": "Finance Data Team",
        "department": "Finance",
        "criticality": "High"
    }
}


# ==================================================
# ASSET TYPES
# ==================================================

asset_types = [
    "Database",
    "Table",
    "Pipeline",
    "Warehouse",
    "Dashboard",
    "Report"
]


# ==================================================
# OTHER VALUES
# ==================================================

environments = [
    "Production",
    "Development",
    "Testing"
]


lifecycles = [
    "Active",
    "Active",
    "Active",
    "Deprecated"
]


data_classifications = [
    "Public",
    "Internal",
    "Confidential",
    "Restricted"
]


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def random_date():

    start_date = date(2025, 1, 1)

    days = random.randint(
        0,
        620
    )

    return (
        start_date
        + timedelta(days=days)
    ).isoformat()


# ==================================================
# CREATE OUTPUT DIRECTORY
# ==================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ==================================================
# ASSET STORAGE
# ==================================================

assets = []

relationships = []

asset_counter = 1


# ==================================================
# CREATE ASSETS
# ==================================================

for domain in domains:

    config = domain_config[
        domain
    ]

    # ------------------------------------------------
    # DATABASE
    # ------------------------------------------------

    database_id = (
        f"A{asset_counter:03d}"
    )

    asset_counter += 1

    assets.append(
        {
            "asset_id": database_id,
            "asset_name": f"{domain} Database",
            "asset_type": "Database",
            "owner": config["owner"],
            "department": config["department"],
            "environment": "Production",
            "criticality": config["criticality"],
            "lifecycle": "Active",
            "data_classification": random.choice(
                data_classifications
            ),
            "location": "Data Center",
            "status": "Healthy",
            "last_updated": random_date(),
            "description":
                f"{domain} source database"
        }
    )


    # ------------------------------------------------
    # TABLES
    # ------------------------------------------------

    table_ids = []

    for table_number in range(1, 4):

        table_id = (
            f"A{asset_counter:03d}"
        )

        asset_counter += 1

        table_ids.append(
            table_id
        )

        table_names = [
            f"{domain} Master Table",
            f"{domain} Transaction Table",
            f"{domain} History Table"
        ]

        assets.append(
            {
                "asset_id": table_id,
                "asset_name":
                    table_names[
                        table_number - 1
                    ],
                "asset_type": "Table",
                "owner": config["owner"],
                "department":
                    config["department"],
                "environment": "Production",
                "criticality":
                    config["criticality"],
                "lifecycle": "Active",
                "data_classification":
                    random.choice(
                        data_classifications
                    ),
                "location": "Data Center",
                "status": "Healthy",
                "last_updated":
                    random_date(),
                "description":
                    f"{domain} data table"
            }
        )

        # Database contains table

        relationships.append(
            {
                "source_asset_id":
                    database_id,
                "target_asset_id":
                    table_id,
                "relationship_type":
                    "contains"
            }
        )


    # ------------------------------------------------
    # PIPELINES
    # ------------------------------------------------

    pipeline_ids = []

    for pipeline_number in range(1, 3):

        pipeline_id = (
            f"A{asset_counter:03d}"
        )

        asset_counter += 1

        pipeline_ids.append(
            pipeline_id
        )

        assets.append(
            {
                "asset_id":
                    pipeline_id,
                "asset_name":
                    f"{domain} ETL Pipeline "
                    f"{pipeline_number}",
                "asset_type":
                    "Pipeline",
                "owner":
                    "Data Engineering",
                "department":
                    config["department"],
                "environment":
                    "Production",
                "criticality":
                    config["criticality"],
                "lifecycle":
                    "Active",
                "data_classification":
                    "Internal",
                "location":
                    "Cloud",
                "status":
                    "Healthy",
                "last_updated":
                    random_date(),
                "description":
                    f"{domain} ETL pipeline"
            }
        )


        # Table feeds pipeline

        source_table = table_ids[
            pipeline_number - 1
        ]

        relationships.append(
            {
                "source_asset_id":
                    source_table,
                "target_asset_id":
                    pipeline_id,
                "relationship_type":
                    "feeds"
            }
        )


    # ------------------------------------------------
    # WAREHOUSE
    # ------------------------------------------------

    warehouse_id = (
        f"A{asset_counter:03d}"
    )

    asset_counter += 1

    assets.append(
        {
            "asset_id":
                warehouse_id,
            "asset_name":
                f"{domain} Data Warehouse",
            "asset_type":
                "Warehouse",
            "owner":
                "BI Team",
            "department":
                config["department"],
            "environment":
                "Production",
            "criticality":
                config["criticality"],
            "lifecycle":
                "Active",
            "data_classification":
                "Internal",
            "location":
                "Cloud",
            "status":
                "Healthy",
            "last_updated":
                random_date(),
            "description":
                f"{domain} analytical warehouse"
        }
    )


    # Pipelines load warehouse

    for pipeline_id in pipeline_ids:

        relationships.append(
            {
                "source_asset_id":
                    pipeline_id,
                "target_asset_id":
                    warehouse_id,
                "relationship_type":
                    "loads"
            }
        )


    # ------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------

    dashboard_id = (
        f"A{asset_counter:03d}"
    )

    asset_counter += 1

    assets.append(
        {
            "asset_id":
                dashboard_id,
            "asset_name":
                f"{domain} Analytics Dashboard",
            "asset_type":
                "Dashboard",
            "owner":
                "Business Intelligence Team",
            "department":
                config["department"],
            "environment":
                "Production",
            "criticality":
                config["criticality"],
            "lifecycle":
                "Active",
            "data_classification":
                "Internal",
            "location":
                "Cloud",
            "status":
                "Healthy",
            "last_updated":
                random_date(),
            "description":
                f"{domain} business dashboard"
        }
    )


    relationships.append(
        {
            "source_asset_id":
                warehouse_id,
            "target_asset_id":
                dashboard_id,
            "relationship_type":
                "feeds"
        }
    )


    # ------------------------------------------------
    # REPORT
    # ------------------------------------------------

    report_id = (
        f"A{asset_counter:03d}"
    )

    asset_counter += 1

    assets.append(
        {
            "asset_id":
                report_id,
            "asset_name":
                f"{domain} Business Report",
            "asset_type":
                "Report",
            "owner":
                "Business Team",
            "department":
                config["department"],
            "environment":
                "Production",
            "criticality":
                config["criticality"],
            "lifecycle":
                "Active",
            "data_classification":
                "Internal",
            "location":
                "Cloud",
            "status":
                "Healthy",
            "last_updated":
                random_date(),
            "description":
                f"{domain} business report"
        }
    )


    relationships.append(
        {
            "source_asset_id":
                warehouse_id,
            "target_asset_id":
                report_id,
            "relationship_type":
                "feeds"
        }
    )


# ==================================================
# CROSS-DOMAIN RELATIONSHIPS
# ==================================================

# Helper dictionary

asset_lookup = {
    asset["asset_name"]:
        asset["asset_id"]
    for asset in assets
}


# ==================================================
# IMPORTANT CROSS-DOMAIN DEPENDENCIES
# ==================================================

cross_dependencies = [

    (
        "Customer Data Warehouse",
        "Marketing Analytics Dashboard"
    ),

    (
        "Customer Data Warehouse",
        "Finance Data Warehouse"
    ),

    (
        "Orders Data Warehouse",
        "Finance Data Warehouse"
    ),

    (
        "Orders Data Warehouse",
        "Marketing Analytics Dashboard"
    ),

    (
        "Product Data Warehouse",
        "Marketing Analytics Dashboard"
    ),

    (
        "Product Data Warehouse",
        "Inventory Data Warehouse"
    ),

    (
        "Supplier Data Warehouse",
        "Inventory Data Warehouse"
    ),

    (
        "Inventory Data Warehouse",
        "Logistics Data Warehouse"
    ),

    (
        "Payment Data Warehouse",
        "Finance Data Warehouse"
    ),

    (
        "Employee Data Warehouse",
        "Finance Data Warehouse"
    )
]


for source_name, target_name in cross_dependencies:

    source_id = asset_lookup.get(
        source_name
    )

    target_id = asset_lookup.get(
        target_name
    )

    if source_id and target_id:

        relationships.append(
            {
                "source_asset_id":
                    source_id,

                "target_asset_id":
                    target_id,

                "relationship_type":
                    "depends_on"
            }
        )


# ==================================================
# ADD SOME EXTRA CROSS-DOMAIN LINKS
# ==================================================

extra_links = [

    (
        "Customer Master Table",
        "Marketing ETL Pipeline 1"
    ),

    (
        "Orders Transaction Table",
        "Finance ETL Pipeline 1"
    ),

    (
        "Product Master Table",
        "Inventory ETL Pipeline 1"
    ),

    (
        "Supplier Master Table",
        "Inventory ETL Pipeline 2"
    ),

    (
        "Payment Transaction Table",
        "Finance ETL Pipeline 2"
    ),

    (
        "Inventory Transaction Table",
        "Logistics ETL Pipeline 1"
    )
]


for source_name, target_name in extra_links:

    source_id = asset_lookup.get(
        source_name
    )

    target_id = asset_lookup.get(
        target_name
    )

    if source_id and target_id:

        relationships.append(
            {
                "source_asset_id":
                    source_id,

                "target_asset_id":
                    target_id,

                "relationship_type":
                    "feeds"
            }
        )


# ==================================================
# ADD ORPHAN ASSETS
# ==================================================

orphan_assets = [

    {
        "asset_id":
            f"A{asset_counter:03d}",

        "asset_name":
            "Legacy Customer Archive",

        "asset_type":
            "Database",

        "owner":
            "Legacy Systems Team",

        "department":
            "IT",

        "environment":
            "Development",

        "criticality":
            "Low",

        "lifecycle":
            "Deprecated",

        "data_classification":
            "Restricted",

        "location":
            "Legacy Server",

        "status":
            "Inactive",

        "last_updated":
            random_date(),

        "description":
            "Legacy disconnected database"
    },

    {
        "asset_id":
            f"A{asset_counter + 1:03d}",

        "asset_name":
            "Unused Marketing Report",

        "asset_type":
            "Report",

        "owner":
            "Marketing Team",

        "department":
            "Marketing",

        "environment":
            "Testing",

        "criticality":
            "Low",

        "lifecycle":
            "Deprecated",

        "data_classification":
            "Internal",

        "location":
            "Cloud",

        "status":
            "Inactive",

        "last_updated":
            random_date(),

        "description":
            "Unused disconnected report"
    }
]


assets.extend(
    orphan_assets
)


# ==================================================
# WRITE ASSETS CSV
# ==================================================

asset_columns = [
    "asset_id",
    "asset_name",
    "asset_type",
    "owner",
    "department",
    "environment",
    "criticality",
    "lifecycle",
    "data_classification",
    "location",
    "status",
    "last_updated",
    "description"
]


with open(
    ASSET_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=asset_columns
    )

    writer.writeheader()

    writer.writerows(
        assets
    )


# ==================================================
# ADD RELATIONSHIP IDS
# ==================================================

relationship_rows = []

for index, relationship in enumerate(
    relationships,
    start=1
):

    relationship_rows.append(
        {
            "relationship_id":
                f"R{index:03d}",

            "source_asset_id":
                relationship[
                    "source_asset_id"
                ],

            "target_asset_id":
                relationship[
                    "target_asset_id"
                ],

            "relationship_type":
                relationship[
                    "relationship_type"
                ]
        }
    )


# ==================================================
# WRITE RELATIONSHIPS CSV
# ==================================================

relationship_columns = [
    "relationship_id",
    "source_asset_id",
    "target_asset_id",
    "relationship_type"
]


with open(
    RELATIONSHIP_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=relationship_columns
    )

    writer.writeheader()

    writer.writerows(
        relationship_rows
    )


# ==================================================
# FINAL INFORMATION
# ==================================================

print()
print("=" * 50)
print("DATASET GENERATED SUCCESSFULLY")
print("=" * 50)

print(
    "Total assets:",
    len(assets)
)

print(
    "Total relationships:",
    len(relationship_rows)
)

print(
    "Assets CSV:",
    ASSET_FILE
)

print(
    "Relationships CSV:",
    RELATIONSHIP_FILE
)

print("=" * 50)