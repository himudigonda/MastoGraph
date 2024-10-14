# Mastodon Analysis Project

This project collects, processes, and analyzes data from Mastodon to perform sentiment analysis and network analysis. The project is structured to collect posts based on specific keywords, process the data, classify the sentiment, and construct a network for further analysis.

## Project Structure

```
mastodon_analysis_project/
├── __pycache__/
├── .gitignore
├── config.py
├── data/
│   ├── processed/
│   │   └── processed_posts.json
│   └── raw/
│       ├── keyword_posts.json
│       └── user_data.json
├── main.py
├── output.out
├── requirements.txt
├── run.sh
└── src/
    ├── __pycache__/
    ├── classification.py
    ├── data_collection.py
    ├── data_processing.py
    ├── network_analysis.py
    └── network_construction.py
```

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd mastodon_analysis_project
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Configure the project:**

    Update the

config.py

 file with your Mastodon API credentials and other configuration parameters.

## Running the Project

To run the project, execute the

run.sh

 script:

```sh
sh run.sh
```

Alternatively, you can run the

main.py

 script directly with the necessary arguments:

```sh
python main.py --collect-data --classify
```

## Project Components

- **Data Collection:** Collects posts from Mastodon based on specified keywords and users. Implemented in

data_collection.py

.
- **Data Processing:** Processes the collected data and saves it to a JSON file. Implemented in

data_processing.py

.
- **Classification:** Classifies the sentiment of the posts. Implemented in

classification.py

.
- **Network Construction:** Constructs a network based on the processed data. Implemented in

network_construction.py

.
- **Network Analysis:** Analyzes the constructed network. Implemented in

network_analysis.py

.

## Configuration

The

config.py

 file contains the configuration parameters for the project, including Mastodon API credentials, keywords, and data collection parameters.

```py
# config.py
MASTODON_CLIENT_ID = 'your_client_id'
MASTODON_CLIENT_SECRET

 =

 'your_client_secret'
MASTODON_ACCESS_TOKEN = 'your_access_token'
MASTODON_API_BASE_URL = 'https://mastodon.social/'

TOPIC = "Your Topic"
KEYWORDS = ["keyword1", "keyword2", "keyword3"]
SEED_USERS = ["user1", "user2", "user3"]

MIN_POSTS = 600
MIN_USERS = 200
```

## Data

- **Raw Data:** Collected raw data is stored in the

raw

 directory.
- **Processed Data:** Processed data is stored in the

processed

 directory.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

This project uses the following libraries:

- Mastodon.py
- NetworkX
- NLTK
- Pandas
- Matplotlib

For a full list of dependencies, see the

requirements.txt

 file.

## Contact

For any questions or issues, please contact [Your Name](mailto:your.email@example.com).

---

This README provides an overview of the project, setup instructions, and details about the various components and their functionalities.
