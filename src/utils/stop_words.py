import nltk

nltk.download("stopwords")

from nltk.corpus import stopwords
from stop_words import get_stop_words

from src.utils.tokenizers import tokenizers

nltk_sw = stopwords.words("russian")
# sw_sw is ignored because of plenty meaningful words
sw_sw = get_stop_words("ru")


def remove_stop_words(text, tokenizer=None):
    if isinstance(text, str):
        text = tokenizers[tokenizer](text) if tokenizer else text.split()

    return [x for x in text if x not in nltk_sw]
