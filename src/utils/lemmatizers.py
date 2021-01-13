"""Lemmatizers for ru lang."""

from pymystem3 import Mystem
from pymorphy2 import MorphAnalyzer
from src.utils.tokenizers import tokenizers

# init outside of function is for better speed
MYSTEM = Mystem()
MORPH = MorphAnalyzer()


def mystem_lemmatizer(text):
    """Mystem3 lemmatizer.

    Args:
        text (str or iterable): text to be lemmatized

    Returns:
        list: list of lemmatized tokens
    """
    if not isinstance(text, str):
        text = " ".join(text)
    return MYSTEM.lemmatize(text)


def pymorphy_lemmatizer(text, tokenizer=None):
    """Pymorphy2 lemmatizer.

    Args:
        text (str or iterable): text to be lemmatized
        tokenizer (str, optional): tokenizer for str `text`.
            If `text` is not str parameter is ignored.
            `None` is whitespace tokenizer.
            Defaults to None.

    Returns:
        list: list of lemmatized tokens
    """
    if isinstance(text, str):
        text = tokenizers[tokenizer](text) if tokenizer else text.split()
    return [MORPH.parse(x)[0].normal_form for x in text]


lemmatizers = {"mystem": mystem_lemmatizer, "pymorphy": pymorphy_lemmatizer}
