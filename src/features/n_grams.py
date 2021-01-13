
from collections import Counter, defaultdict
from itertools import chain

from nltk.util import ngrams

from src.utils.tokenizers import tokenizers


def get_n_grams_dict(dataset, grams=1, tokenizer=None):
    tokenizer = tokenizers[tokenizer] if tokenizer else tokenizer['whitespace']
    rus_tokenized = [tokenizer(x) for x in dataset]
    rus_ngramed = [list(ngrams(x, grams)) for x in rus_tokenized]

    counter = Counter(chain(*rus_ngramed)).most_common()
    del (rus_ngramed, rus_tokenized)

    main_dict = defaultdict(dict)

    for keys, num in counter:
        main_dict[keys[0]][keys[1]] = num
    return main_dict


def get_n_grams(dataset, grams=1, tokenizer=None):
    tokenizer = tokenizers[tokenizer] if tokenizer else tokenizer['whitespace']
    rus_tokenized = [tokenizer(x) for x in dataset]
    rus_ngramed = [list(ngrams(x, grams)) for x in rus_tokenized]
    del rus_tokenized
    return Counter(chain(*rus_ngramed)).most_common()


def get_n_grams_mem_eff(dataset, grams=1, tokenizer=None):
    tokenizer = tokenizers[tokenizer] if tokenizer else tokenizer['whitespace']
    counter = Counter()
    for record in dataset:
        n_grams = ngrams(tokenizer(record), grams)
        counter.update(Counter(n_grams))
    return counter.most_common()
