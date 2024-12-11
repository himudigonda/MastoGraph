# Mastodon Analysis Project

## Overview

This project demonstrates the collection, processing, and analysis of social media data from the Mastodon platform. The project aims to classify toxic content, construct social networks, and perform network analysis using various machine learning models and graph-based techniques.

Key aspects include:
- **Social Media Data Crawling** using the Mastodon API.
- **Natural Language Processing (NLP)** techniques for sentiment and toxicity analysis.
- **Graph Theory** and **Network Analysis** for exploring social interactions and content propagation.
- **Machine Learning Models** such as Llama3-8B for text classification.

## Technologies Used

- **Mastodon API**: For collecting real-time social media data using keyword-based and user-based data scraping.
- **Python**: The core programming language for implementing all data collection, processing, classification, and analysis functionalities.
- **NetworkX**: Used for constructing and analyzing networks of interactions between users and posts.
- **LangChain & OllamaLLM (Llama3-8B)**: Large Language Models used for classifying content based on toxicity.
- **TextBlob**: A natural language processing library used for sentiment analysis.
- **Matplotlib & Seaborn**: For visualizing network properties, including degree distribution, PageRank, and community detection.
- **Pandas**: For data processing and manipulation.
- **Community-Louvain**: Used for community detection within networks.

## Project Components

### 1. **Data Collection**

The project collects data from Mastodon based on:
- **Keyword-based search**: Collects posts that match certain keywords relevant to the topic of "Twitter vs. Mastodon" (e.g., `#TwitterVsMastodon`, `#MastodonIsBetter`).
- **User-based search**: Collects data on users, their followers, and followees.

**Technologies**: Mastodon API, Mastodon.py

**Files**: `data_collection.py`, `config.py`

### 2. **Data Processing**

Raw data collected from Mastodon is cleaned and processed to extract relevant features such as:
- Cleaning HTML tags from posts.
- Extracting user details.
- Calculating sentiment scores using TextBlob.

**Technologies**: BeautifulSoup, TextBlob, Pandas

**Files**: `data_processing.py`

### 3. **Network Construction**

We create two types of networks based on the processed data:
- **Information Diffusion Network**: A directed network where nodes represent posts and edges indicate interactions (e.g., replies, mentions).
- **Friendship Network**: An undirected network of users connected by follower-followee relationships.

**Technologies**: NetworkX

**Files**: `network_construction.py`

### 4. **Toxicity Classification**

The **Llama3-8B** model from OllamaLLM is used to classify posts as **toxic** or **non-toxic**. Toxicity is determined based on abusive language or harmful content within posts. Each post in the Information Diffusion Network is assigned a toxicity score on a scale from 0 to 1.

**Technologies**: LangChain, OllamaLLM, Llama3-8B

**Files**: `classification.py`

### 5. **Network Analysis**

After constructing the networks, various **network measures** are calculated, including:
- **Degree Distribution**: A histogram of the node degrees.
- **PageRank**: Ranking of nodes based on their influence within the network.
- **Clustering Coefficient**: Measures how tightly connected a node's neighborhood is.
- **Betweenness Centrality**: A measure of the node's influence on information flow.
- **Community Detection**: Using the Louvain method to detect communities within the network.

**Technologies**: NetworkX, Matplotlib, Seaborn, Community-Louvain

**Files**: `network_analysis.py`

### 6. **Visualization**

The network measures and community structures are visualized using Matplotlib and Seaborn:
- **Degree Distribution** is visualized in a log-log plot.
- **PageRank and Betweenness Centrality** visualizations show the importance of nodes in the network.
- **Community Detection** visualizes clusters of closely connected nodes.

**Technologies**: Matplotlib, Seaborn

## Project Structure

```
mastodon_analysis_project/
├── README.md               # Project overview and instructions
├── config.py               # Configuration file for API keys and data collection parameters
├── data/
│   ├── processed/          # Processed data files
│   └── raw/                # Raw data files
├── main.py                 # Main script to run data collection, classification, and analysis
├── requirements.txt        # Python dependencies
├── run.sh                  # Shell script to run the project
└── src/
    ├── classification.py   # Toxicity classification implementation
    ├── data_collection.py  # Data collection from Mastodon
    ├── data_processing.py  # Data processing and cleaning
    ├── network_analysis.py # Network measures and visualization
    └── network_construction.py  # Network construction for posts and users
```

## Setup and Usage

1. Clone the repository:
```
git clone <repository_url>
cd mastodon_analysis_project
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Configure the project:

Update the config.py file with your Mastodon API credentials, keywords, and user seeds.

```python
# config.py
MASTODON_CLIENT_ID = 'your_client_id'
MASTODON_CLIENT_SECRET = 'your_client_secret'
MASTODON_ACCESS_TOKEN = 'your_access_token'
MASTODON_API_BASE_URL = 'https://mastodon.social/'
```

4. Running the Project

Run the project using the provided shell script:
```bash
sh run.sh
```
Alternatively, you can run the main.py script with arguments:
```bash
python main.py --collect-data --classify
```

This will:

- Collect data from Mastodon.
- Process and classify posts.
- Construct and analyze the social networks.

Results and Insights

This project results in the creation of two main social networks:

- Information Diffusion Network of posts.
- Friendship Network of users.

Through toxicity analysis and network measures, the project provides valuable insights into how information spreads on Mastodon and how toxic content may propagate through social networks.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements

- Mastodon.py: For accessing the Mastodon API.
- LangChain & OllamaLLM: For providing the Llama3-8B model used in toxicity classification.
- NetworkX: For network construction and analysis.
- TextBlob: For sentiment analysis.
- Matplotlib & Seaborn: For visualizations.
