import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
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
    degrees = [d for n, d in G.degree()]
    return sum(degrees) / len(degrees)



def visualize_network(G, measure, title, filename):
    plt.figure(figsize=(25, 25))  # Increase the figure size for better visibility
    pos = nx.spring_layout(G, k=0.2)  # Adjust k for better spacing

    # Normalize the measure for node sizes
    norm = Normalize(vmin=min(measure.values()), vmax=max(measure.values()))
    node_sizes = [norm(measure[node]) * 1000 for node in G.nodes()]  # Scale node sizes

    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue', alpha=0.6)
    edges = nx.draw_networkx_edges(G, pos, alpha=0.3)

    # Add labels for larger nodes
    labels = {node: node for node, size in zip(G.nodes(), node_sizes) if size > 200}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color='black')

    plt.title(f"{title} Visualization")
    plt.axis('off')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust layout manually
    plt.savefig(filename)
    plt.close()

def detect_communities(G):
    partition = community_louvain.best_partition(G)
    modularity = community_louvain.modularity(partition, G)
    return partition, modularity
