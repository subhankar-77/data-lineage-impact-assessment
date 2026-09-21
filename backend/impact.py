from lineage import create_lineage_graph
import networkx as nx



def calculate_impact(graph, asset_id):

    direct_impact = list(graph.successors(asset_id))

    all_downstream = list(nx.descendants(graph, asset_id))

    transitive_impact = [
        asset for asset in all_downstream
        if asset not in direct_impact
    ]

    return direct_impact, transitive_impact


def get_upstream_assets(graph, asset_id):

    return list(graph.predecessors(asset_id))



def calculate_risk_level(graph, asset_id):

    direct_impact, transitive_impact = calculate_impact(
        graph,
        asset_id
    )

    total_impact = len(direct_impact) + len(transitive_impact)

    if total_impact >= 5:
        return "HIGH"

    elif total_impact >= 3:
        return "MEDIUM"

    else:
        return "LOW"



def display_impact(graph, asset_id):

    asset_name = graph.nodes[asset_id]["name"]

    direct_impact, transitive_impact = calculate_impact(
        graph,
        asset_id
    )

    upstream = get_upstream_assets(graph, asset_id)

    print("\n===== IMPACT ASSESSMENT =====")

    print("\nSelected Asset:")
    print(asset_name)

    print("\nUpstream Assets:")

    if upstream:

        for asset in upstream:
            print("-", graph.nodes[asset]["name"])

    else:
        print("None")

    print("\nDirect Impact:")

    if direct_impact:

        for asset in direct_impact:
            print("-", graph.nodes[asset]["name"])

    else:
        print("None")

    print("\nTransitive Impact:")

    if transitive_impact:

        for asset in transitive_impact:
            print("-", graph.nodes[asset]["name"])

    else:
        print("None")

    total_impact = len(direct_impact) + len(transitive_impact)

    total_assets = graph.number_of_nodes()

    impact_percentage = (
        total_impact / total_assets
    ) * 100

    risk_level = calculate_risk_level(
        graph,
        asset_id
    )

    print("\nTotal Affected Assets:", total_impact)

    print(
        "Impact Percentage:",
        round(impact_percentage, 2),
        "%"
    )

    print("Risk Level:", risk_level)


if __name__ == "__main__":

    graph = create_lineage_graph()

    print("===== AVAILABLE ASSETS =====\n")

    for asset_id, data in graph.nodes(data=True):

        print(
            asset_id,
            "-",
            data["name"]
        )

    print()

    asset_id = input(
        "Enter asset ID to assess impact: "
    )

    if asset_id in graph:

        display_impact(
            graph,
            asset_id
        )

    else:

        print("Asset ID not found.")