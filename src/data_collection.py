import json
from mastodon import Mastodon
from config import *
from datetime import datetime
from tqdm import tqdm
import time

mastodon = Mastodon(
    client_id=MASTODON_CLIENT_ID,
    client_secret=MASTODON_CLIENT_SECRET,
    access_token=MASTODON_ACCESS_TOKEN,
    api_base_url=MASTODON_API_BASE_URL
)

def convert_datetime(obj):
    if isinstance(obj, dict):
        return {k: convert_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def collect_keyword_data():
    posts = []
    for keyword in tqdm(KEYWORDS, desc="Scraping keywords"):
        max_id = None
        keyword_posts = []
        while len(keyword_posts) < MIN_POSTS // len(KEYWORDS):
            try:
                results = mastodon.timeline_hashtag(keyword, max_id=max_id, limit=40)
                if not results:
                    break
                keyword_posts.extend(results)
                max_id = results[-1]['id']
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"Error collecting data for keyword {keyword}: {e}")
                time.sleep(5)  # Wait longer on error
        posts.extend(keyword_posts)

    # Convert datetime objects to strings
    posts = convert_datetime(posts)

    with open('data/raw/keyword_posts.json', 'w') as f:
        json.dump(posts[:MIN_POSTS], f, indent=2)

    print(f"Collected {len(posts[:MIN_POSTS])} posts based on keywords")

def collect_user_data():
    users = set()
    for seed_user in tqdm(SEED_USERS, desc="Scraping user data"):
        try:
            user_id = mastodon.account_lookup(seed_user)['id']
            followers = mastodon.account_followers(user_id)
            following = mastodon.account_following(user_id)
            users.update([user['id'] for user in followers + following])
            if len(users) >= MIN_USERS:
                break
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Error collecting data for user {seed_user}: {e}")
            time.sleep(5)  # Wait longer on error

    user_data = []
    for user_id in tqdm(list(users)[:MIN_USERS], desc="Fetching user details"):
        try:
            user_info = mastodon.account(user_id)
            user_info['followers'] = mastodon.account_followers(user_id)
            user_info['following'] = mastodon.account_following(user_id)
            user_data.append(user_info)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Error fetching data for user ID {user_id}: {e}")

    # Convert datetime objects to strings
    user_data = convert_datetime(user_data)

    with open('data/raw/user_data.json', 'w') as f:
        json.dump(user_data, f, indent=2)

    print(f"Collected data for {len(user_data)} users")
