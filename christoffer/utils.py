from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import interactive # FIXME - MIGHT BECOME USEFULL


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


def create_wordcloud(size_dict,
                     color_dict = None,
                     title = "Wordcloud",
                     bigrams = False,
                     show = True,
                     save_path = None):
    
    wordcloud = WordCloud(background_color ='white',
                          stopwords = set(STOPWORDS),
                          collocations = bigrams, # Allow / disallow bigrams
                          contour_color = "black",
                          relative_scaling = 1,
                          min_font_size = 10).generate_from_frequencies(size_dict)
    
    word_freqs = wordcloud.words_ if color_dict is None else color_dict
    wordcloud.recolor(color_func= _my_tf_color_func(word_freqs))

    # plot the WordCloud image                    
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    
    if save_path:
        plt.savefig(save_path)
    
    if show:
        plt.show()
    
"""
def create_wordcloud(size_dict,
                     color_dict = None,
                     title = "Wordcloud",
                     #img_mask = "masks/money_bag_mask.png",
                     bigrams = False,
                     show = True,
                     height = 200,
                     width = 400,
                     save_path = None):
    
    #custom_mask = np.array(Image.open(img_mask))
    wordcloud = WordCloud(background_color ='white',
                          stopwords = set(STOPWORDS),
                          collocations = bigrams, # Allow / disallow bigrams
                          width = 400,
                          height = height,
                          #mask = custom_mask,
                          contour_color = "black",
                          min_font_size = 10).generate_from_frequencies(size_dict)
    
    #word_freqs = wordcloud.words_ if color_dict is None else color_dict
    #wordcloud.recolor(color_func= _my_tf_color_func(word_freqs))

    # plot the WordCloud image               
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    
    if save_path:
        plt.savefig(save_path)
    
    if show:
        plt.show()
    
"""