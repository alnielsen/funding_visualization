import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from math import inf, floor, isnan
import plotly.express as px
import plotly.graph_objects as go

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


def _color_scaling(val, new_min = 15, new_max = 60, old_min = 0, old_max = 100):
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


def _clean_desc_col(desc_col: list):
    """
    Removes nans and converts col to str
    """
    desc_col_clean = []
    for desc in desc_col:
        if ( isinstance(desc, float) or isinstance(desc, int) ) and isnan(desc):
            desc_col_clean.append("")
        else:
            desc_col_clean.append(str(desc))  
    return desc_col_clean

def get_stop_words() -> str:
    """
    Returns a list of stopwords
    """
    # Danish stopwords
    txt = open("stopord.txt", "r", encoding='utf-8')
    file_content = txt.read()
    danish_stopwords = file_content.split("\n")
    txt.close()
    
    # English stopwords
    stopwords = list(STOPWORDS)
    
    # custom stopwords
    cust_stop_w = ["-", "–", "samt", "både", "række", "hvilket", "findes", "give", "øget", "ofte", "giver", "del", "projektet", "udviklingen", "baseret", "studier"]
    
    # Combine english and danish
    stopwords.extend(danish_stopwords)
    stopwords.extend(cust_stop_w)
    
    return stopwords
    


####################
# Public functions #
####################
# Data functions:
#   - Generate data
#   - dict to df

# Wordcloud functions:
#   - plot wc
#   - create_wordcloud

# Bar plot functions
#   - create_bar_plot


# ----- Data functions ------
def dict_to_df(data_dict):
    """
    Converts a word - value (such af word - frequency) dict to a dataframe
    """
    return pd.DataFrame({"word": data_dict.keys(), "value": data_dict.values()})



def generate_data(df: pd.DataFrame, funding_thresh_hold: int) -> tuple[dict, dict]:
    """
    Generatives three word: value dictionaries:
    - word: funding
    - word: average funding
    - word: frequency
    """
    
    df["title_desc"] = df["Titel"] + _clean_desc_col(df["Beskrivelse"])
    
    freqs = {} # Absolute frequencies
    funding = {} # Absolute funding recieved
    stopwords = get_stop_words()
    
    # Create dict of absolute freqs and funding
    for text, amount in zip(df["title_desc"], df["Bevilliget beløb"]):
        # Split each token/word on whitespace
        tokens = list(set([token.lower() for token in text.split()])) # Get unique tokens
        # COunt unique tokens in each grant application
        prev_tokens = []
        for token in tokens:
            token = token.lower()
            if token in stopwords or token in prev_tokens:
                continue
                
            else:
                prev_tokens.append(token)
                if not token in freqs:
                    freqs[token] = 1
                    funding[token] = amount
                else:
                    freqs[token] += 1
                    funding[token] += amount

    funding = _filter_dict(funding, funding_thresh_hold)
    freqs = _make_same_keys(funding, freqs)
    
    avg_funding = {}
    for key in funding:   
        avg_funding[key] =  funding[key] // freqs[key]
        
    return (avg_funding, funding, freqs)


# ------ Word cloud functions ------ 
def plot_wc(wordcloud, title = "Word cloud", show= True, save_path = None):
    """
    Plots a word cloud
    """                  
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
    """
    Returns a word cloud
    """
    
    wordcloud = WordCloud(background_color ='white',
                          stopwords = set(STOPWORDS),
                          collocations = bigrams, # Allow / disallow bigrams
                          contour_color = "black",
                          relative_scaling = 1,
                          min_font_size = 10).generate_from_frequencies(size_dict)
    
    word_freqs = wordcloud.words_ if color_dict is None else color_dict
    wordcloud.recolor(color_func= _my_tf_color_func(word_freqs))
    
    return wordcloud

# ------ Bar plots ------
def create_bar_plot(data_dict,
                    color_dict,
                    color_label = "color label",
                    value_label = "value label",
                    title = "No Title",
                    top_n = 25):
    """
    Takes as word: value dict such as
    word: frequency
    Returns as ploty plot
    """
    df_dict = {"Word": [], "value": [], "color": []}
    for key, val, in data_dict.items():
        df_dict["Word"].append(key)
        df_dict["value"].append(val)
        df_dict["color"].append(color_dict[key])
        
    df = pd.DataFrame(df_dict)
    df = df.sort_values(by="value", ascending = False)
    df = df.head(top_n)
    df = df.sort_values(by = "value", ascending=True)
    # I have no Idea why I have to sort it in ascending order to get the words with highest value on top
    fig = px.bar(df,
                  x="value",
                  y = "Word",
                  labels = {"value": value_label,
                            "color": color_label},
                  color = "color",
                  color_continuous_scale = px.colors.sequential.Redor, 
                  title = title)
    
    if max(df["color"]) <= 5:
        tick = 1
    else:
        tick = int((max(df["color"])/5))
    fig.update_layout(coloraxis={"colorbar":{"dtick":tick}})
    return fig
        
def create_line_plot(df):
    """
    Returns a plotly lineplot with years on x-axis and value and y axis
    """
    print("MOCK Implementation")
    

if __name__ == "__main__":
    pass



