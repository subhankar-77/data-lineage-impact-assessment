# 🔗 Data Lineage & Impact Assessment
Group project for Data Lineage and Impact Assessment - NPN Hackathon (Cognizant)



A prototype system for **asset discovery, data lineage exploration, and change impact assessment** — built for the NPN Hackathon (Cognizant).

The tool models an organization's data assets (databases, tables, pipelines, warehouses, dashboards, reports) as a **undirected dependency graph**, and lets a user pick any asset to see:
- what feeds into it (**upstream**)
- what it directly feeds (**direct downstream impact**)
- everything downstream of that, however many hops away (**transitive impact**)
- a computed **risk level** for changing/breaking that asset
- a downloadable **Change Impact Report**

---

## ✨ Features

- **Asset Catalog** — searchable, filterable registry of all data assets
- **Lineage Graph** — built with NetworkX from CSV-sourced relationship data
- **Upstream / Downstream Lookup** — immediate parents and children of any asset
- **Impact Assessment** — direct vs. transitive downstream impact, with an impact-percentage and a HIGH / MEDIUM / LOW risk score
- **Visual Lineage Graph** — interactive subgraph visualization (matplotlib) centered on the selected asset
- **Change Impact Report** — exportable as CSV
- **Orphan Asset Detection** — flags assets with no lineage connections at all
- **Project & Asset-Type Statistics** — coverage, node/edge counts, type breakdown

---

## 🏗️ Architecture

```
generate_dataset.py          → synthetic assets.csv & relationships.csv
        │
        ▼
data/assets.csv, data/relationships.csv
        │
        ▼
backend/database.py          → loads CSVs into SQLite (lineage.db)
        │
        ▼
backend/assets.py            → asset registry (search / filter / CRUD)
backend/lineage.py           → builds the NetworkX DiGraph, upstream/downstream lookups
backend/impact.py            → direct/transitive impact + risk scoring
        │
        ▼
frontend/app.py              → Streamlit UI (catalog, graph, impact report)
```

**Tech stack:** Python, Streamlit, SQLite, NetworkX, Pandas, Matplotlib

---

## 📁 Project Structure

```
data_lineage_impact_assesment/
├── backend/
│   ├── database.py       # CSV → SQLite loader
│   ├── assets.py         # asset registry (search, filter, add, get)
│   ├── lineage.py        # lineage graph construction & traversal
│   └── impact.py         # impact calculation & risk scoring
├── data/
│   ├── assets.csv         # generated asset metadata
│   └── relationships.csv  # generated asset relationships
├── frontend/
│   └── app.py             # Streamlit dashboard
├── generate_dataset.py    # synthetic dataset generator
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/subhankar-77/data-lineage-impact-assesment.git
cd data-lineage-impact-assesment
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash

```

---

## ▶️ Running the Project

The project has three stages: **generate data → build the database → launch the app**. Run them in order from the repository root.

### Step 1 — Generate the dataset (optional, already included)
Regenerates `data/assets.csv` and `data/relationships.csv` from scratch:
```bash
python generate_dataset.py
```

### Step 2 — Build the SQLite database
Loads the CSVs into `lineage.db`:
```bash
cd backend
python database.py
cd ..
```

### Step 3 — Launch the Streamlit app
```bash
streamlit run frontend/app.py
```

This opens the dashboard in your browser (default: `http://localhost:8501`).

---

## 🧪 Testing Individual Modules

Each backend module can be run standalone for quick checks:

```bash
cd backend

python assets.py     # test asset registry: list all, search by keyword, filter by type
python lineage.py    # build the graph and print upstream/downstream for a sample asset
python impact.py     # interactive: pick an asset ID and print a full impact assessment
```

---

## 📊 Sample Data Model

**Assets** (`data/assets.csv`): `asset_id, asset_name, asset_type, owner, department, environment, criticality, lifecycle, data_classification, location, status, last_updated, description`

**Relationships** (`data/relationships.csv`): `relationship_id, source_asset_id, target_asset_id, relationship_type`

The synthetic dataset models 10 business domains (Customer, Orders, Employee, Product, Payment, Inventory, Marketing, Logistics, Supplier, Finance), each with a `Database → Tables → Pipelines → Warehouse → Dashboard/Report` chain, plus deliberate cross-domain dependencies and a couple of orphan (disconnected) assets to demonstrate orphan detection.

---

## 🔮 Future Improvements

- Weight risk scoring by asset criticality/environment, not just downstream count
- Cache the graph build in Streamlit (`st.cache_data`) instead of rebuilding on every rerun
- Support live connections to real data catalogs (e.g., OpenLineage, dbt manifest, Airflow) instead of static CSVs
- Cycle detection/validation on the dependency graph

---

## 👥 Contributors

Built for the NPN Hackathon (Cognizant).

## 📄 License

This project is provided as-is for educational/hackathon purposes, and is made by Team CoreShift.
