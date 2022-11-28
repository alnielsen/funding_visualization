import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from math import inf, floor, isnan
import plotly.express as px
import plotly.graph_objects as go
from typing import Literal

####################
# Helper functions #
####################
def _make_same_keys(filtered_dict: dict,
                    non_filtered_dict: int) -> dict:
    """
    Creates a dict, which contains the same keys as another dictionary, while still keeping the original values
    """
    return_dict = {}
    for key in filtered_dict:
        val = non_filtered_dict[key]
        return_dict[key] = val
    return return_dict


def _filter_dict(dictionary: dict,
                 lower_thresh: int = 0,
                 upper_thresh: int = inf) -> dict:
    """
    Removes key: value pairs, where the value is not between lower_thresh and upper_thresh
    """
    filtered_dict = {}
    for key, val in dictionary.items(): 
        if  lower_thresh <= val <= upper_thresh:
            filtered_dict[key] = val
    return filtered_dict


def _get_remaining_perc(val: int | float) -> int | float:
    """
    Returns the remaining percent of a value 
    """
    return 100 - val


def _color_scaling(val: int | float,
                   new_min: int |float = 15,
                   new_max = 60, old_min = 0, old_max = 100) -> int | float:
    """
    Convert from a scaling of 0 to 100 to a new range for colors
    """
    val = _get_remaining_perc(val)
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((val - old_min) * new_range) / old_range) + new_min


def scale_word_dict(word_dict: dict) -> dict:
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


def _my_tf_color_func(dictionary: dict) -> "function":
    """
    A colorfunction for the wordcloud which scales a dictionary and applies a colorfunction to each word
    """
    dictionary = scale_word_dict(dictionary)
    def my_tf_color_func_inner(word, font_size, position, orientation, random_state=None, **kwargs):
        return f"hsl(1, 100%, {dictionary[word]}%)"
    return my_tf_color_func_inner


def _clean_desc_col(desc_col: list):
    """
    Removes nans and converts col to str from the descriotion column
    """
    desc_col_clean = []
    for desc in desc_col:
        if ( isinstance(desc, float) or isinstance(desc, int) ) and isnan(desc):
            desc_col_clean.append("")
        else:
            desc_col_clean.append(str(desc))  
    return desc_col_clean


def get_stop_words(stopword_path: str = "stopord.txt") -> list[str]:
    """
    Description
    ------------
    Returns a list of stopwords

    Parameters
    ----------
    stopword_path (str): The path a txt file with stopwords

    Preconditions
    -------------
    The stopwords in the txt-file are seperated by a newline
    """
    # Danish stopwords
    txt = open(stopword_path, "r", encoding='utf-8')
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

def dict_to_df(data_dict: dict) -> pd.DataFrame:
    """
    Description
    -----------
    Converts a word - value (such af word - frequency) dict to a dataframe

    Parameters
    ----------
    data_dict (dict): a dictionary where the keys are word and they have and associated value
    """
    return pd.DataFrame({"word": data_dict.keys(), "value": data_dict.values()})



def generate_data(df: pd.DataFrame,
                  funding_thresh_hold: int = 0) -> tuple[dict, dict, dict]:
    """
    Description
    -----------
    Generatives three key: value dictionaries where the key is a word:
    - word: funding
    - word: average funding
    - word: frequency

    Parameters
    ----------
    - df (pandas.DataFrame): A dataframe containing the following columns: 
        - "År" (int), "Titel" (str), "Beskrivelse" (str), "Bevilliget beløb" (int | float)
    - funding_thresh_hold (int): Only get words which have a higher funding than this
        - Default: 0

    Return
    ------
    tuple(dict, dict, dict)
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
def plot_wc(wordcloud,
            title: str = "Word cloud",
            show= True,
            save_path = None) -> None:
    """
    Description
    ------------
    Plots a word cloud

    Parameters
    ----------
    - wordcloud: a matplotlib.pyplot object containing a wordcloud
    - title (str): The title for the plot
        - Default; 'Word cloud'
    - show (bool): Show the plot
        - Default: True
    - save_path: Path to save the plot as a png. If None it will not be saved.
        - Default: None
    
    Return
    ------
    None
    """                  
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    
    if show:
        plt.show()


def create_wordcloud(size_dict: dict,
                     color_dict: bool = None,
                     bigrams: bool = False) -> plt:
    """
    Description
    ------------
    Generate af wordcloud

    Parameters
    -----------
    - size_dict (dict): a word - value dict to determine the size of each word.
    - color_dict (dict): a word - value dict to determine the size of each word.
    - bigrams (bool): Allow bigrams
        - Default: False
    
    Return
    ------
    matplotlib.pyplot object which contains a wordcloud

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
                    top_n = 25) -> px.bar:
    """
    Description
    ------------
    Takes as word: value dict and returns as ploty plot
    
    Parameters
    -----------
    - data_dict (dict): A dict where the keys are word and the words associated value. 
      Can be created with the function generate_data(df, funding_thresh).The value determines the size of a word' bar
      Examples of dicts:
        - word: freqency
        - word: funding
        - word: average funding
    - color_dict (dict): A word value dict (like previously), however the value determines the bar color for a word.
    - color_label (str): The label for the colorbar
    - value_label (str): The label for the x_axis
    - title (str): The title of the plot.
    - top_n (int): Only take the top n keys with the highest value.
    
    Return
    -------
    plotly.express.bar 
    
    Preconditions
    -------------
    - data_dict and color_dict contains the same keys.
    
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

# ----- Bubble charts ------
def gen_bubble_data(df: pd.DataFrame,
                    top_n: int | None = None,
                    sort_col: Literal["freqs", "funding", "avg_funding"] | None = None,
                    words: list[str] | None = None ) -> pd.DataFrame:
    """
    Description
    ------------
    Generates a dataset for bubble charts which can be filterede accorng to words, and/or value of a column
    
    Parameters
    ------------
    - df (pandas.DataFrame): A dataframe containing the following columns: 
      "År" (int), "Titel" (str), "Beskrivelse" (str), "Bevilliget beløb" (int | float)
    - top_n (int | None): The number of highest valued words to choose. If None then all words are chosen.
    - sort_col ("freqs" | "funding", "avg_funding"): The column/value to choose the top_n words from.
        - freqs = choose the top_n most used words each year. If None, the words are not sorted.
        - funding = Choose the top_n most funded words each year
        - avg_funding = Choose the top_n words with the highest average funding each year
    - words (list[str]): A list of strings if you only which to get data for the given words.

    Return
    ------
    A pandas.DataFrame with the following columns:
        - word (str): The word
        - freqs (int): The amount of grants the word is mentioned in.
        - avg_funding (int | float): The average funidng for each grant the word appears in.
        - funding (int | float): The total funding for all papers the word appears in.
        - year (int): The year data is extracted from.
    The dataframe is sorted by year
    """
    years = list(set(df["År"]))
    years.sort()
    df_dict = {"word": [], "freqs": [], "funding": [], "avg_funding": [], "year": []}
    for year in years:
        temp_df = df[df["År"] == year]
        avg_funding, funding, freqs = generate_data(df = temp_df,
                                                    funding_thresh_hold = 0)
        for key in funding: 
            if words is None:         
                df_dict["word"].append(key)
                df_dict["freqs"].append(freqs[key])
                df_dict["funding"].append(funding[key])
                df_dict["avg_funding"].append(avg_funding[key])
                df_dict["year"].append(year)
            elif words is not None and key in words:
                df_dict["word"].append(key)
                df_dict["freqs"].append(freqs[key])
                df_dict["funding"].append(funding[key])
                df_dict["avg_funding"].append(avg_funding[key])
                df_dict["year"].append(year)
    df = pd.DataFrame(df_dict)

    sorted_df = pd.DataFrame(columns = ["word", "freqs", "funding", "avg_funding", "year"])
    for year in years:
        temp_df = df[df["year"] == year]
        
        if sort_col is not None:
            temp_df = temp_df.sort_values(by=sort_col, ascending = False)
        if top_n is not None:
            temp_df = temp_df.head(top_n)
            
        sorted_df = pd.concat([sorted_df, temp_df], ignore_index = True)

    return sorted_df.sort_values(by="year")

def create_bubble_plot(df: pd.DataFrame, 
                       x_col: str,
                       y_col: str,
                       size_col: str,
                       color_col: str,
                       x_strech: int = 0,
                       y_strech: int = 0,
                       max_bub_size: int = 55,
                       title: str = "Title",
                       x_lab: str | None = None,
                       y_lab: str | None = None,
                       size_lab: str | None = None,
                       color_lab: str | None = None) -> px.scatter:
    """
    Description
    ------------
    Creates a bubble chart displaying the words funding, frequency and average frequency over time.

    Parameters
    ----------
    - A pandas.DataFrame with the following columns:
        - word (str): The word
        - freqs (int): The amount of grants the word is mentioned in.
        - avg_funding (int | float): The average funidng for each grant the word appears in.
        - funding (int | float): The total funding for all papers the word appears in.
        - year (int): The year data is extracted from.
        - The dataframe is sorted by year
    - x_col (str): The column name in df for the values of the x-axis
    - y_col (str): The column name in df for the values of the y-axis
    - size_col( str): The column name in df for the values of which will determine the size of the bubbles
    - color_col (str): The column name in df for the values of which will determine the color of the bubbles
    - x_strech (int): Padding which are added to the x axis 
        - So if min value is 50 and max value is 100 and x_strech is 25 then the x axis will start at 25 and end at 125
        - Default: 0
    - y_strech (int): Padding which are added to the y axis 
        - So if min value is 50 and max value is 100 and y_strech is 25 then the y axis will start at 25 and end at 125
        - Default: 0
    - max_bub_size (int): The max bubble sizes
        - Default: 55
    - title (str): The title of the bubble chart
    - x_lab (str): The labels for the x values
        - Default: x_col
    y_lab (str): The labels for the y values
        - Default: y_col
    size_lab: The label for the value determining the bubble size
        - Default: size_col
    color_lab: The label for the colorbar
        - Default: color_col
    
    Return
    -------
    plotly.express.scatter
    """
    
    if x_lab == None:
        x_lab = x_col
    if y_lab == None:
        y_lab = y_col
    if size_lab == None:
        size_lab = size_col
    if color_lab == None:
        color_lab = color_col
    fig = px.scatter(df,
                     x=x_col,
                     y=y_col,
                     color= list(df[color_col]),
                     color_continuous_scale=px.colors.sequential.Redor,
                     animation_frame="year",
                     animation_group = "word",
                     size = list(df[size_col]),
                     hover_name="word",
                     size_max = max_bub_size,
                     text = "word",
                     title = title,
                     range_x=[min(df[x_col] - x_strech), max(df[x_col]) + x_strech],
                     range_y=[min(df[y_col]) - y_strech, max(df[y_col]) + y_strech],
                     labels={
                     x_col: x_lab,
                     y_col: y_lab,
                     size_col: size_lab,
                     "year": "Year"
                 }
                    )
    fig["layout"].pop("updatemenus") # Remove buttons (it does not work when animating)
    fig.update_layout(coloraxis_colorbar_title_text = color_lab)
    
    hovertemplate="<br>".join([
        f"{x_lab}: " + "%{x:,.0f}",
        f"{y_lab}: " + "%{y}",
        f"{size_lab}: " + "%{marker.size:,.0f}"])

    fig.update_traces(hovertemplate=hovertemplate)
    for frame in fig.frames:
        frame.data[0].hovertemplate = hovertemplate
    return fig

if __name__ == "__main__":
    pass



