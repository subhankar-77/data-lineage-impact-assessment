import streamlit as st
import sys
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# ==================================================
# BACKEND PATH
# ==================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "backend"
        )
    )
)


from lineage import create_lineage_graph

from impact import (
    calculate_impact,
    get_upstream_assets,
    calculate_risk_level
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Data Lineage & Impact Assessment",
    page_icon="🔗",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🔗 Data Lineage & Impact Assessment")

st.write(
    "Asset discovery, lineage exploration and "
    "change impact assessment."
)

st.divider()


# ==================================================
# CREATE LINEAGE GRAPH
# ==================================================

graph = create_lineage_graph()


# ==================================================
# CREATE ASSET DATAFRAME
# ==================================================

asset_rows = []

for asset_id, data in graph.nodes(data=True):

    asset_rows.append(
        {
            "Asset ID": asset_id,
            "Asset Name": data["name"],
            "Asset Type": data["type"]
        }
    )


asset_df = pd.DataFrame(asset_rows)


# ==================================================
# PROJECT OVERVIEW
# ==================================================

st.subheader("📊 Project Overview")


total_assets = graph.number_of_nodes()

total_relationships = graph.number_of_edges()


# Assets that have at least one relationship
connected_assets = [
    node
    for node in graph.nodes
    if graph.degree(node) > 0
]


connected_asset_count = len(
    connected_assets
)


# Orphan assets
orphan_assets = [
    node
    for node in graph.nodes
    if graph.degree(node) == 0
]


orphan_count = len(
    orphan_assets
)


# Coverage
if total_assets > 0:

    asset_coverage = (
        connected_asset_count
        / total_assets
    ) * 100

else:

    asset_coverage = 0


# Lineage coverage
if total_assets > 0:

    lineage_coverage = (
        connected_asset_count
        / total_assets
    ) * 100

else:

    lineage_coverage = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Assets",
        total_assets
    )


with col2:

    st.metric(
        "Relationships",
        total_relationships
    )


with col3:

    st.metric(
        "Asset Coverage",
        f"{asset_coverage:.1f}%"
    )


with col4:

    st.metric(
        "Orphan Assets",
        orphan_count
    )


st.divider()


# ==================================================
# ASSET CATALOG
# ==================================================

st.subheader("🔍 Asset Catalog")


# Search box

search_text = st.text_input(
    "Search by Asset ID or Asset Name",
    placeholder="Example: Customer"
)


# Asset type filter

available_types = sorted(
    asset_df["Asset Type"].unique()
)


selected_types = st.multiselect(
    "Filter by Asset Type",
    available_types,
    default=available_types
)


# Apply search

filtered_df = asset_df.copy()


if search_text:

    search_lower = search_text.lower()

    filtered_df = filtered_df[
        filtered_df["Asset ID"]
        .str.lower()
        .str.contains(
            search_lower,
            na=False
        )
        |
        filtered_df["Asset Name"]
        .str.lower()
        .str.contains(
            search_lower,
            na=False
        )
    ]


# Apply type filter

filtered_df = filtered_df[
    filtered_df["Asset Type"].isin(
        selected_types
    )
]


st.write(
    f"Showing {len(filtered_df)} "
    f"of {total_assets} assets"
)


st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==================================================
# ASSET SELECTION
# ==================================================

st.subheader("🎯 Select Asset for Analysis")


asset_ids = list(graph.nodes)


asset_names = {
    asset_id:
        graph.nodes[asset_id]["name"]
    for asset_id in asset_ids
}


selected_asset = st.selectbox(
    "Select an Asset",
    asset_ids,
    format_func=lambda asset_id:
        f"{asset_id} - {asset_names[asset_id]}"
)


selected_name = graph.nodes[
    selected_asset
]["name"]


selected_type = graph.nodes[
    selected_asset
]["type"]


# ==================================================
# SELECTED ASSET INFORMATION
# ==================================================

st.subheader("📋 Asset Information")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Asset ID",
        selected_asset
    )


with col2:

    st.metric(
        "Asset Name",
        selected_name
    )


with col3:

    st.metric(
        "Asset Type",
        selected_type
    )


with col4:

    st.metric(
        "Total Assets",
        total_assets
    )


st.divider()


# ==================================================
# LINEAGE CALCULATION
# ==================================================

upstream = get_upstream_assets(
    graph,
    selected_asset
)


direct_impact, transitive_impact = calculate_impact(
    graph,
    selected_asset
)


# ==================================================
# UPSTREAM / DOWNSTREAM
# ==================================================

st.subheader("🔗 Lineage Information")


col1, col2 = st.columns(2)


with col1:

    st.markdown("### ⬆️ Upstream Assets")

    if upstream:

        for asset_id in upstream:

            st.write(
                f"• {asset_id} - "
                f"{graph.nodes[asset_id]['name']}"
            )

    else:

        st.info(
            "No upstream assets."
        )


with col2:

    st.markdown(
        "### ⬇️ Direct Downstream Assets"
    )

    if direct_impact:

        for asset_id in direct_impact:

            st.write(
                f"• {asset_id} - "
                f"{graph.nodes[asset_id]['name']}"
            )

    else:

        st.info(
            "No direct downstream assets."
        )


st.divider()


# ==================================================
# VISUAL LINEAGE
# ==================================================

st.subheader("📊 Visual Lineage")


lineage_nodes = set()

lineage_nodes.add(
    selected_asset
)


for asset in upstream:

    lineage_nodes.add(
        asset
    )


for asset in direct_impact:

    lineage_nodes.add(
        asset
    )


for asset in transitive_impact:

    lineage_nodes.add(
        asset
    )


lineage_graph = graph.subgraph(
    lineage_nodes
).copy()


if lineage_graph.number_of_nodes() > 0:

    position = nx.spring_layout(
        lineage_graph,
        seed=42
    )


    fig, ax = plt.subplots(
        figsize=(12, 7)
    )


    nx.draw_networkx_nodes(
        lineage_graph,
        position,
        node_size=1800
    )


    nx.draw_networkx_edges(
        lineage_graph,
        position,
        arrows=True,
        arrowsize=20
    )


    labels = {}

    for node in lineage_graph.nodes:

        labels[node] = (
            node
            + "\n"
            + graph.nodes[node]["name"]
        )


    nx.draw_networkx_labels(
        lineage_graph,
        position,
        labels=labels,
        font_size=8
    )


    ax.set_title(
        "Asset Lineage Graph"
    )


    ax.axis("off")


    st.pyplot(
        fig
    )


else:

    st.warning(
        "No lineage information available."
    )


st.divider()


# ==================================================
# IMPACT ASSESSMENT
# ==================================================

st.subheader(
    "⚠️ Impact Assessment"
)


total_impact = (
    len(direct_impact)
    +
    len(transitive_impact)
)


if total_assets > 0:

    impact_percentage = (
        total_impact
        /
        total_assets
    ) * 100

else:

    impact_percentage = 0


risk_level = calculate_risk_level(
    graph,
    selected_asset
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Direct Impact",
        len(direct_impact)
    )


with col2:

    st.metric(
        "Transitive Impact",
        len(transitive_impact)
    )


with col3:

    st.metric(
        "Total Affected",
        total_impact
    )


with col4:

    st.metric(
        "Impact %",
        f"{impact_percentage:.2f}%"
    )


st.markdown(
    f"### Risk Level: **{risk_level}**"
)


st.divider()


# ==================================================
# CHANGE IMPACT REPORT
# ==================================================

st.subheader(
    "📄 Change Impact Report"
)


report_data = []


# Direct impact

for asset_id in direct_impact:

    report_data.append(
        {
            "Asset ID":
                asset_id,

            "Asset Name":
                graph.nodes[
                    asset_id
                ]["name"],

            "Asset Type":
                graph.nodes[
                    asset_id
                ]["type"],

            "Impact Type":
                "Direct",

            "Selected Asset":
                selected_asset,

            "Risk Level":
                risk_level
        }
    )


# Transitive impact

for asset_id in transitive_impact:

    report_data.append(
        {
            "Asset ID":
                asset_id,

            "Asset Name":
                graph.nodes[
                    asset_id
                ]["name"],

            "Asset Type":
                graph.nodes[
                    asset_id
                ]["type"],

            "Impact Type":
                "Transitive",

            "Selected Asset":
                selected_asset,

            "Risk Level":
                risk_level
        }
    )


if report_data:

    report_df = pd.DataFrame(
        report_data
    )


    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True
    )


    csv_data = report_df.to_csv(
        index=False
    )


    st.download_button(
        label="📥 Download Impact Report",
        data=csv_data,
        file_name=(
            f"impact_report_"
            f"{selected_asset}.csv"
        ),
        mime="text/csv"
    )


else:

    st.info(
        "No downstream assets are affected."
    )


st.divider()


# ==================================================
# ORPHAN ASSETS
# ==================================================

st.subheader(
    "⚠️ Orphan Asset Analysis"
)


if orphan_assets:

    st.warning(
        f"{orphan_count} orphan asset(s) "
        "were found."
    )


    orphan_data = []


    for asset_id in orphan_assets:

        orphan_data.append(
            {
                "Asset ID":
                    asset_id,

                "Asset Name":
                    graph.nodes[
                        asset_id
                    ]["name"],

                "Asset Type":
                    graph.nodes[
                        asset_id
                    ]["type"]
            }
        )


    orphan_df = pd.DataFrame(
        orphan_data
    )


    st.dataframe(
        orphan_df,
        use_container_width=True,
        hide_index=True
    )


else:

    st.success(
        "No orphan assets found."
    )


st.divider()


# ==================================================
# ASSET TYPE SUMMARY
# ==================================================

st.subheader(
    "📊 Asset Type Summary"
)


type_summary = (
    asset_df[
        "Asset Type"
    ]
    .value_counts()
    .reset_index()
)


type_summary.columns = [
    "Asset Type",
    "Count"
]


st.dataframe(
    type_summary,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==================================================
# PROJECT STATISTICS
# ==================================================

st.subheader(
    "📈 Project Statistics"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Nodes",
        graph.number_of_nodes()
    )


with col2:

    st.metric(
        "Total Edges",
        graph.number_of_edges()
    )


with col3:

    if total_assets > 0:

        st.metric(
            "Lineage Coverage",
            f"{lineage_coverage:.1f}%"
        )

    else:

        st.metric(
            "Lineage Coverage",
            "0%"
        )


st.divider()


# ==================================================
# FOOTER
# ==================================================

st.caption("""
    Data Lineage & Impact Assessment 
    \n CTS Hackathon Project
    \n Developed by: Team CoreShift

""")

