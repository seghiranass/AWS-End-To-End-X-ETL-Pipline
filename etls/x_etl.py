import sys
import pandas as pd
import tweepy
import re


def connect_x(BEARER_TOKEN):
    try:
        client  = tweepy.Client(BEARER_TOKEN, wait_on_rate_limit=False)
        print("connected to X!")
        return client
    except Exception as e:
        print("Connection failed:" ,e)
        sys.exit(1)

def extract_data(client, query="Palestine", max_results=10):
    """
    Fetch recent tweets about 'Palestine' with engagement and timestamp info.
    """
    response = client.search_recent_tweets(
        query=query + " -is:retweet lang:en",  # remove retweets, keep English tweets
        tweet_fields=["id", "text", "created_at", "public_metrics"],
        max_results=max_results
    )

    if not response.data:
        print("No tweets found.")
        return pd.DataFrame()

    tweets = []
    for tweet in response.data:
        tweets.append({
            "id": tweet.id,
            "created_at": tweet.created_at,
            "text": tweet.text,
            "retweets": tweet.public_metrics.get("retweet_count", 0),
            "likes": tweet.public_metrics.get("like_count", 0)
        })

    df = pd.DataFrame(tweets)
    print(f"Extracted {len(df)} tweets about Palestine.")
    return df

def clean_text(text):
    text = re.sub(r"http\S+", "", text)     # remove URLs
    text = re.sub(r"@\S+", "", text)        # remove mentions
    text = re.sub(r"#", "", text)           # remove hashtags
    text = re.sub(r"\n+", " ", text)        # remove line breaks
    return text.strip().lower()

def transform_data(df: pd.DataFrame):
    """
    Cleans and enriches tweet data with sentiment and emotion labels.
    """
    if df.empty:
        print("No data to transform.")
        return df

    df['text'] = df['text'].apply(clean_text)

    # Filter out very short or meaningless tweets
    df = df[df['text'].str.len() > 20]

    return df

def load_data_to_csv(df: pd.DataFrame, path: str):
    if df.empty:
        print("Nothing to save.")
        return
    df.to_csv(path, index=False, encoding='utf-8')
    print(f"Saved {len(df)} processed tweets to {path}")