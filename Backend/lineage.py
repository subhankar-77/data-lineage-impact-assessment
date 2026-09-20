import sqlite3
import networkx as nx

DB_NAME = "lineage.db"


def create_lineage_graph():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    # Get asset information
    cursor.execute("""
        SELECT asset_id, asset_name, asset_type
        FROM assets
    """)

    assets = cursor.fetchall()

    # Get relationships
    cursor.execute("""
        SELECT source_asset_id, target_asset_id
        FROM relationships
    """)

    relationships = cursor.fetchall()

    connection.close()

    graph = nx.DiGraph()

    # Add assets as nodes
    for asset_id, asset_name, asset_type in assets:

        graph.add_node(
            asset_id,
            name=asset_name,
            type=asset_type
        )

    # Add relationships
    for source, target in relationships:

        graph.add_edge(source, target)

    return graph


def get_upstream(graph, asset_id):

    return list(graph.predecessors(asset_id))


def get_downstream(graph, asset_id):

    return list(graph.successors(asset_id))


def get_all_downstream(graph, asset_id):

    return nx.descendants(graph, asset_id)


if __name__ == "__main__":

    graph = create_lineage_graph()

    print("===== LINEAGE GRAPH =====")

    print("Number of nodes:", graph.number_of_nodes())

    print("Number of relationships:", graph.number_of_edges())

    asset_id = "A002"

    print("\n===== SELECTED ASSET =====")

    print(graph.nodes[asset_id]["name"])

    print("\n===== UPSTREAM =====")

    upstream = get_upstream(graph, asset_id)

    for asset in upstream:
        print(graph.nodes[asset]["name"])

    print("\n===== DIRECT DOWNSTREAM =====")

    downstream = get_downstream(graph, asset_id)

    for asset in downstream:
        print(graph.nodes[asset]["name"])

    print("\n===== ALL DOWNSTREAM =====")

    all_downstream = get_all_downstream(graph, asset_id)

    for asset in all_downstream:
        print(graph.nodes[asset]["name"])