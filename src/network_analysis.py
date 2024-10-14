from community import community_louvain
from collections import Counter
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

def calculate_degree_distribution(G):
    degrees = [d for n, d in G.degree()]
    degree_counts = Counter(degrees)
    x, y = zip(*sorted(degree_counts.items()))

    plt.figure(figsize=(10, 6))
    plt.loglog(x, y, 'b.')
    plt.title("Degree Distribution (log-log scale)")
    plt.xlabel("Degree")
    plt.ylabel("Count")
    plt.savefig("degree_distribution.png")
    plt.close()

def calculate_additional_measures(G):
    print("Calculating additional network measures...")
    clustering = nx.average_clustering(G)
    pagerank = nx.pagerank(G)
    betweenness = nx.betweenness_centrality(G)
    eigenvector = nx.eigenvector_centrality(G)

    return {
        "clustering": clustering,
        "pagerank": pagerank,
        "betweenness": betweenness,
        "eigenvector": eigenvector
    }

def analyze_average_friends(G):
    local_avg = sum(dict(G.degree()).values()) / len(G)
    global_avg = nx.average_degree_connectivity(G)
    return {"local_avg": local_avg, "global_avg": global_avg}

def visualize_network(G, measure, title, filename):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=20, node_color='lightblue', with_labels=False)

    node_colors = [measure[node] for node in G.nodes()]
    norm = Normalize(vmin=min(node_colors), vmax=max(node_colors))
    sm = ScalarMappable(cmap=plt.cm.viridis, norm=norm)
    sm.set_array([])

    # Normalize node colors
    normalized_colors = [norm(color) for color in node_colors]

    nodes = nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_colors, cmap=plt.cm.viridis)

    # Create colorbar
    plt.colorbar(sm, ax=plt.gca(), label=title)
    plt.title(f"{title} Visualization")
    plt.axis('off')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust layout manually
    plt.savefig(filename)
    plt.close()


def detect_communities(G):
    partition = community_louvain.best_partition(G)
    modularity = community_louvain.modularity(partition, G)
    return partition, modularity

# Example usage
if __name__ == "__main__":
    # Assume G is your network
    G = nx.karate_club_graph()  # Example graph, replace with your actual network

    calculate_degree_distribution(G)
    measures = calculate_additional_measures(G)
    avg_friends = analyze_average_friends(G)

    print("Average friends:", avg_friends)

    visualize_network(G, measures['pagerank'], "PageRank", "pagerank_visualization.png")
    visualize_network(G, measures['betweenness'], "Betweenness Centrality", "betweenness_visualization.png")

    partition, modularity = detect_communities(G)
    print(f"Detected {len(set(partition.values()))} communities with modularity {modularity:.4f}")
