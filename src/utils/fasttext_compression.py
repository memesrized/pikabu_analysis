import sys

import compress_fasttext
from gensim.models.fasttext import load_facebook_model


def compress_fasttext_model(input_path, output_path):
    big_model = load_facebook_model(input_path).wv
    small_model = compress_fasttext.prune_ft_freq(big_model, pq=True)
    small_model.save(output_path)


if __name__ == "__main__":
    compress_fasttext_model(sys.argv[1], sys.argv[2])
