from segtok.tokenizer import word_tokenizer


def whitespace_tokenizer(text):
    return text.split()


tokenizers = {"whitespace": whitespace_tokenizer, "segtok": word_tokenizer}
