"""Additional processing for data."""
import json

import pandas as pd

from src import PROJECT_PATHS


def one_hot_tag_encoder(df):
    """Encode list of tags as one-hot-encoder inplace.

    Retains only related tags from config.

    Args:
        df (pandas.DataFrame): Dataframe to be encoded.
    """
    with open(PROJECT_PATHS.configs / "related_tags.json") as file_:
        tags_dict = json.load(file_)
    df["TAGS"] = df["TAGS"].str.split('|')
    for tag in tags_dict:
        df[tag] = 0
        for i in df.index:
            for post_tag in df["TAGS"][i]:
                if post_tag in tags_dict[tag]:
                    df[tag][i] = 1
                    break


if __name__ == "__main__":
    df = pd.read_csv(PROJECT_PATHS.data / "processed" / "peeled.csv")
    one_hot_tag_encoder(df)
    df.to_csv(PROJECT_PATHS.data / "processed" / "one_hot_encoded.csv")
