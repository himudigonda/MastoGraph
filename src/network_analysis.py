import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from community import community_louvain
from collections import Counter
import seaborn as sns

# Set global plot style
plt.style.use('seaborn-v0_8-dark-palette')

def calculate_degree_distribution(G):
    degrees = [d for n, d in G.degree()]
    degree_counts = Counter(degrees)
    x, y = zip(*sorted(degree_counts.items()))

    plt.figure(figsize=(10, 6))
    plt.loglog(x, y, 'b.', markersize=8)
    plt.title("Degree Distribution (log-log scale)", fontsize=16)
    plt.xlabel("Degree", fontsize=14)
    plt.ylabel("Count", fontsize=14)
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig("degree_distribution.png", bbox_inches='tight')
    # plt.show()

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

def analyze_local_and_global_friends(G):
    # Global average (already implemented)
    degrees = [d for n, d in G.degree()]
    global_average_friends = sum(degrees) / len(degrees)

    # Local average (1-hop friends) for each node
    local_averages = {}
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        local_degrees = [G.degree(neighbor) for neighbor in neighbors]  # Degree of 1-hop neighbors
        if len(local_degrees) > 0:
            local_averages[node] = sum(local_degrees) / len(local_degrees)  # Average of 1-hop friends
        else:
            local_averages[node] = 0  # No neighbors means no 1-hop friends

    # Calculate overall local average
    overall_local_average = sum(local_averages.values()) / len(local_averages)

    print(f"Global Average Friends: {global_average_friends}")
    print(f"Overall Local Average (1-hop) Friends: {overall_local_average}")

    return global_average_friends, overall_local_average

def visualize_network(G, measure, title, filename):
    plt.figure(figsize=(10, 6))  # Increase figure size for better visibility
    pos = nx.spring_layout(G, k=0.15, iterations=100)  # Adjust layout for better spacing

    # Normalize the measure for node sizes and colors
    norm = Normalize(vmin=min(measure.values()), vmax=max(measure.values()))
    node_sizes = [norm(measure[node]) * 1500 for node in G.nodes()]  # Scale node sizes
    node_colors = [measure[node] for node in G.nodes()]  # Node color based on measure

    # Draw nodes with size and color based on the measure
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap='coolwarm', alpha=0.85)
    edges = nx.draw_networkx_edges(G, pos, alpha=0.3)

    # Add labels: Display usernames instead of IDs if available
    labels = {node: G.nodes[node].get('username', node) for node, size in zip(G.nodes(), node_sizes) if size > 500}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color='black')

    # Add color bar
    sm = ScalarMappable(cmap='coolwarm', norm=norm)
    sm.set_array(node_colors)  # Map the node colors to the ScalarMappable
    plt.colorbar(sm, ax=plt.gca())  # Pass the current Axes to the colorbar

    plt.title(f"{title} Visualization", fontsize=20)
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight')
    # plt.show()

def detect_communities(G):
    partition = community_louvain.best_partition(G)
    modularity = community_louvain.modularity(partition, G)
    return partition, modularity
