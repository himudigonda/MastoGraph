import argparse
from src import data_collection, data_processing, network_construction, classification, network_analysis

def main(args):
    if args.collect_data:
        print("Collecting data...")
        data_collection.collect_keyword_data()
        data_collection.collect_user_data()

    print("Processing data...")
    posts = data_processing.load_and_process_data('data/raw/keyword_posts.json')
    users = data_processing.load_and_process_data('data/raw/user_data.json')

    data_processing.save_processed_data(posts, 'data/processed/processed_posts.json')

    print("Constructing networks...")
    info_network = network_construction.build_information_diffusion_network(posts)
    friend_network = network_construction.build_friendship_network(users)

    if args.classify:
        print("Classifying toxicity...")
        if info_network.number_of_nodes() > 0:
            info_network = classification.classify_toxicity(info_network)
        else:
            print("Information diffusion network is empty. Skipping classification.")

    print("Analyzing networks...")
    if friend_network.number_of_nodes() > 0:
        network_analysis.calculate_degree_distribution(friend_network)
        measures = network_analysis.calculate_additional_measures(friend_network)
        avg_friends = network_analysis.analyze_average_friends(friend_network)
        print("Network measures:", measures)
        print("Average friends:", avg_friends)

        network_analysis.visualize_network(friend_network, measures['pagerank'], "PageRank", "pagerank_visualization.png")
        network_analysis.visualize_network(friend_network, measures['betweenness'], "Betweenness Centrality", "betweenness_visualization.png")

        partition, modularity = network_analysis.detect_communities(friend_network)
        print(f"Detected {len(set(partition.values()))} communities with modularity {modularity:.4f}")

        # Explicitly show the final answers and measures
        print("\nFinal Network Measures:")
        print(f"Clustering Coefficient: {measures['clustering']}")
        print(f"PageRank: {measures['pagerank']}")
        print(f"Betweenness Centrality: {measures['betweenness']}")
        print(f"Eigenvector Centrality: {measures['eigenvector']}")
        print(f"Average Friends: {avg_friends}")
        print(f"Number of Communities: {len(set(partition.values()))}")
        print(f"Modularity: {modularity:.4f}")
    else:
        print("Friendship network is empty. Skipping network analysis.")

    print("Analysis completed. Check the generated visualizations and results.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mastodon Network Analysis")
    parser.add_argument('--collect-data', action='store_true', help='Collect new data from Mastodon')
    parser.add_argument('--classify', action='store_true', help='Perform toxicity classification')
    args = parser.parse_args()
    main(args)
