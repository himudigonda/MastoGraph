import networkx as nx
from datetime import datetime

def build_information_diffusion_network(posts):
    G = nx.DiGraph()
    for post in posts:
        G.add_node(post['id'],
                   content=post['content'],
                   user=post['username'],
                   created_at=post['created_at'],
                   sentiment=post['sentiment'])
        for mention in post['mentions']:
            G.add_edge(post['id'], mention, weight=1)
        # Add edges for replies and reblogs with varying weights
        if 'in_reply_to_id' in post and post['in_reply_to_id']:
            G.add_edge(post['id'], post['in_reply_to_id'], weight=2)
        if 'reblog' in post and post['reblog']:
            G.add_edge(post['id'], post['reblog']['id'], weight=3)
    return G

def build_friendship_network(users):
    G = nx.Graph()
    for user in users:
        G.add_node(user['id'],
                   username=user['username'],
                   followers_count=user['followers_count'],
                   following_count=user['following_count'])
        for follower in user['followers']:
            G.add_edge(user['id'], follower['id'], relationship='follower')
        for following in user['following']:
            G.add_edge(user['id'], following['id'], relationship='following')
    return G

def prune_network(G, min_weight=1, min_degree=1):
    # Remove nodes and edges below threshold
    to_remove = [node for node, degree in dict(G.degree()).items() if degree < min_degree]
    G.remove_nodes_from(to_remove)
    if G.is_directed():
        G.remove_edges_from((u, v) for (u, v, d) in G.edges(data=True) if d['weight'] < min_weight)
    return G
