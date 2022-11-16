import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from math import inf

####################
# Helper functions #
####################
def _make_same_keys(filtered_dict, non_filtered_dict):
    """
    Creates a dict, which contains the same keys as another dictionary, while still keeping the original values
    """
    return_dict = {}
    for key in filtered_dict:
        val = non_filtered_dict[key]
        return_dict[key] = val
    return return_dict


def _filter_dict(dictionary, lower_thresh = 0, upper_thresh = inf):
    filtered_dict = {}
    for key, val in dictionary.items(): 
        if  lower_thresh <= val <= upper_thresh:
            filtered_dict[key] = val
    return filtered_dict


def _get_remaining_perc(val: float):
    """
    Returns the remaining percent  
    """
    return 100 - val


def _color_scaling(val, new_min = 15, new_max = 90, old_min = 0, old_max = 100):
    """
    Convert from a scaling of 0 to 100 to a new range for colors
    """
    val = _get_remaining_perc(val)
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((val - old_min) * new_range) / old_range) + new_min


def scale_word_dict(word_dict):
    """
    Scales word freqs to color scalings
    """
    min_val = min(word_dict.values())
    max_val = max(word_dict.values())
    scaled_dict = {}
    for key, val in word_dict.items():
        z = ((val - min_val) / (max_val - min_val)) * 100 #Scaling to between 0 and 100
        scaled_dict[key] = _color_scaling(z)
    return scaled_dict


def _my_tf_color_func(dictionary):
    dictionary = scale_word_dict(dictionary)
    def my_tf_color_func_inner(word, font_size, position, orientation, random_state=None, **kwargs):
        return f"hsl(1, 100%, {dictionary[word]}%)"
    return my_tf_color_func_inner

####################
# Public functions #
####################
# - Generate data
# - plot wc
# - create_wordcloud

def generate_data(df: pd.DataFrame, funding_thresh_hold: int) -> tuple[dict, dict]:
    df["title_desc"] = df["Titel"] #+ df["beskrivelse"]
    freqs = {} # Absolute frequencies
    funding = {} # Absolute funding recieved 
    stopwords = list(set(STOPWORDS))
    stopwords.append("-")
    stopwords.append("–")
    
    # Create dict of absolute freqs and funding
    for text, amount in zip(df["title_desc"], df["Bevilliget beløb"]):
        # Split each token/word on whitespace
        tokens = list(set([token.lower() for token in text.split()])) # Get unique tokens
        # COunt unique tokens in each grant application
        for token in text.split():
            token = token.lower()
            if token in stopwords:
                continue
            if not token in freqs:
                freqs[token] = 1
                funding[token] = amount
            else:
                freqs[token] += 1
                funding[token] += amount

    funding = _filter_dict(funding, funding_thresh_hold)
    freqs = _make_same_keys(funding, freqs)
    return (funding, freqs)


def plot_wc(wordcloud, title, show, save_path = None):
        # plot the WordCloud image                    
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    
    if show:
        plt.show()

def create_wordcloud(size_dict,
                     color_dict = None,
                     bigrams = False):
    
    wordcloud = WordCloud(background_color ='white',
                          stopwords = set(STOPWORDS),
                          collocations = bigrams, # Allow / disallow bigrams
                          contour_color = "black",
                          relative_scaling = 1,
                          min_font_size = 10).generate_from_frequencies(size_dict)
    
    word_freqs = wordcloud.words_ if color_dict is None else color_dict
    wordcloud.recolor(color_func= _my_tf_color_func(word_freqs))
    
    return wordcloud



"""
Example -- How to use
>>> dataframe = pd.read_csv("../gustav/dff.csv")
>>> funding_thresh = 50000
>>> funding, freqs = generate_data(df = dataframe,
                                   funding_thresh_hold = funding_thresh)
>>> w_cloud = create_wordcloud(size_dict = funding,
                               color_dict = freqs)
"""