import pandas as pd

from etls.x_etl import connect_x, extract_data, transform_data, load_data_to_csv
from utils.constants import BEARER_TOKEN, OUTPUT_PATH


def x_pipeline(file_name: str='palestine_tweets.csv'):
    # connecting to X instance
    instance = connect_x(BEARER_TOKEN)
    tweets_data = extract_data(instance, query="Palestine", max_results=10)
    # extraction
    if not tweets_data:
        print("No data to save.")
        return "no_data"
    df_raw = pd.read_csv(tweets_data)
    
    tweets_df = transform_data(df_raw)
    # loading to csv
    file_path = f'{OUTPUT_PATH}/{file_name}'
    load_data_to_csv(tweets_df, file_path)

    return file_path