import json
from bs4 import BeautifulSoup
import re
from textblob import TextBlob

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

def process_post(post):
    cleaned_content = clean_html(post['content'])
    return {
        'id': post['id'],
        'content': cleaned_content,
        'created_at': post['created_at'],
        'username': post['account']['username'],
        'mentions': [mention['username'] for mention in post['mentions']],
        'tags': [tag['name'] for tag in post['tags']],
        'reblogs_count': post['reblogs_count'],
        'favourites_count': post['favourites_count'],
        'replies_count': post['replies_count'],
        'sentiment': get_sentiment(cleaned_content)
    }

def process_user(user):
    return {
        'id': user['id'],
        'username': user['username'],
        'created_at': user['created_at'],
        'followers_count': user['followers_count'],
        'following_count': user['following_count'],
        'statuses_count': user['statuses_count'],
        'last_status_at': user.get('last_status_at', None),
        'followers': [{'id': follower['id'], 'username': follower['username']} for follower in user.get('followers', [])],
        'following': [{'id': following['id'], 'username': following['username']} for following in user.get('following', [])]
    }
def load_and_process_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} records from {file_path}")

    if 'content' in data[0]:
        processed_data = [process_post(post) for post in data]
        print(f"Processed {len(processed_data)} posts")
    else:
        processed_data = [process_user(user) for user in data]
        print(f"Processed {len(processed_data)} users")

    return processed_data

def save_processed_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)
    print(f"Saved processed data to {file_path}")

# Example usage
if __name__ == "__main__":
    raw_posts = load_and_process_data('data/raw/keyword_posts.json')
    save_processed_data(raw_posts, 'data/processed/processed_posts.json')
