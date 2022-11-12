import pandas as pd
from utils import _visualize_word_cloud


def generate_wordcloud(year: int = None, show: bool = False, save_path: str = None):

    df = pd.read_csv("../synthetic_data.csv")
    if year is not None:
        df = df[df["år"] == year]
    df["title_desc"] = df["titel"] + df["beskrivelse"]

    n_words = 0
    funding_sum = sum(df["beløb"])

    abs_freqs = {} # Absolute frequencies
    rel_freqs = {} # Relative frequencies
    abs_funding = {} # Absolute funding recieved
    rel_funding = {}# Relative funding recieved

    # Create dict of absolute freqs and funding
    for text, amount in zip(df["title_desc"], df["beløb"]):
        # Split each token/word on whitespace
        tokens = text.split()
        n_words += len(tokens)
        for token in text.split():
            token = token.lower()
            if not token in abs_freqs:
                abs_freqs[token] = 1
                abs_funding[token] = amount
            else:
                abs_freqs[token] += 1
                abs_funding[token] += amount

    # Create dict for relative freqs
    for key, val in abs_freqs.items():
        rel_freqs[key] = val/n_words

    # Create dict for relative funding
    for key, val in abs_funding.items():
        rel_funding[key] = val/funding_sum
    
    return _visualize_word_cloud(abs_funding, abs_freqs, show, save_path)

for year in range(2013, 2022 + 1):
    f_path = f"output/wordcloud_{year}.jpg"
    w_cloud = generate_wordcloud(year, show = False, save_path = f_path)
    w_cloud.show()
