"""Main data preparation after crawling step."""
import os
import re

import pandas as pd

from regex import UNICODE, VERBOSE, compile
from src import PROJECT_PATHS


def load_parsed(path=PROJECT_PATHS.data / "raw"):
    """Load bunch of csvs.

    Args:
        path (str, optional): Path to directory with crawled data.
            Defaults to PROJECT_PATHS.data/'raw'.

    Returns:
        pandas.DataFrame: Gathered data.
    """
    df = pd.DataFrame()
    for csv in os.listdir(path):
        df = df.append(pd.read_csv(path + csv))
    return df


def remove_html_tags(df, text_col="TEXT", substitute=""):
    """Replace html tags with space.

    May cause texts removal such as <sample text>.
    """
    regexp = re.compile(r"<[^<>]*>")

    df[text_col] = df[text_col].map(lambda x: regexp.sub(substitute, x))


def remove_urls(df, text_col="TEXT", substitute=""):
    """Replace urls with space."""

    def replace_url(string):
        sub = r"""
        (?<=^|[\s<"'(\([{])            # visual border
        (                             # RFC3986-like URIs:
            [A-z]+                    # required scheme
            ://                       # required hier-part
            (?:[^@]+@)?               # optional user
            (?:[\w-]+\.)+\w+          # required host
            (?::\d+)?                 # optional port
            (?:\/[^?\#\s'">)\]}]*)?   # optional path
            (?:\?[^\#\s'">)\]}]+)?    # optional query
            (?:\#[^\s'">)\]}]+)?      # optional fragment
        |                             # simplified e-Mail addresses:
            [\w.#$%&'*+/=!?^`{|}~-]+  # local part
            @                         # klammeraffe
            (?:[\w-]+\.)+             # (sub-)domain(s)
            \w+                       # TLD
        )(?=[\s>"')\)]}]|$)            # visual border
        """
        sub = compile(sub, UNICODE | VERBOSE)
        return sub.sub(substitute, string)

    df[text_col] = df[text_col].map(replace_url)


def remove_punctuation(df, text_col="TEXT", substitute=" "):
    def replace_punctuation(text):
        sub = r"""['!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~']+"""
        return re.sub(sub, substitute, text)

    df[text_col] = df[text_col].map(replace_punctuation)


def remove_by_length(df, text_col="TEXT", len_=500):
    """Remove records with length greater than len_.

    Args:
        df (pandas.DataFrame): data.
        text_col (str, optional): Column with main text. Defaults to "TEXT".
        len_ (int, optional): threshold to cut. Defaults to 500.
    """
    df.drop(index=df[df[text_col].str.len() > len_].index, inplace=True)


if __name__ == "__main__":
    df = load_parsed()
    remove_by_length(df)
    remove_html_tags(df)
    remove_urls(df)
    remove_punctuation(df)
    df.to_csv(PROJECT_PATHS.data / "processed" / "peeled.csv")
