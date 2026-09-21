import sqlite3
import networkx as nx

DB_NAME = "../lineage.db"

def create_lineage_graph():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    #Get asset info
    cursor.execute("""Select asset_id, asset_name, asset_type from assets""")
    assets = cursor.fetchall()

    #Get relationships
    cursor.execute("""Select source_asset_id, target_asset_id from relationships""")
    relationships = cursor.fetchall()

    connection.close()

    graph = nx.DiGraph()

    #Add assets as nodes
    for asset_id, asset_name, asset_type in assets:
        graph.add_node(asset_id, name=asset_name, type=asset_type)

    #Add relationships
    for source, target in relationships:
        graph.add_edge(source, target)

    return graph

def get_upstream(graph, asset_id):
    upstream = list(graph.predecessors(asset_id))
    return upstream

def get_downstream(graph, asset_id):
    downstream = list(graph.successors(asset_id))
    return downstream

# if __name__ == "__main__":
#     graph = create_lineage_graph()
#     print(" LINEAGE GRAPH ")
#     print("Number of nodes : ", graph.number_of_nodes())
#     print("Number of relationships : ", graph.number_of_edges())
#     print("\n Lineage:")
#     for source, target in graph.edges():
#         source_name = graph.nodes[source]["name"]
#         target_name = graph.nodes[target]["names"]
#         print(source, " -> ", target)

if __name__ == "__main__":
    graph = create_lineage_graph()
    asset_id = "A002"
    print("\n SELECTED ASSET")
    print(graph.nodes[asset_id]["name"])
    upstream = get_upstream(graph, asset_id)
    downstream = get_downstream(graph, asset_id)

    print("\n UPSTREAM ")
    for asset in upstream :
        print(graph.nodes[asset]["name"])

    print("\n DOWNSTREAM ")
    for asset in downstream :
        print(graph.nodes[asset]["name"])