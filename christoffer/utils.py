from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


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


def my_tf_color_func(dictionary):
    dictionary = scale_word_dict(dictionary)
    def my_tf_color_func_inner(word, font_size, position, orientation, random_state=None, **kwargs):
        return f"hsl(1, 100%, {dictionary[word]}%)"
    return my_tf_color_func_inner


def _visualize_word_cloud(freqs, color_freqs = None, show = True, save_path = None):
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = set(STOPWORDS),
                    collocations = False, # Allow bigrams
                    min_font_size = 10).generate_from_frequencies(freqs)
    
    word_freqs = wordcloud.words_ if color_freqs is None else color_freqs
    wordcloud.recolor(color_func=my_tf_color_func(word_freqs))

    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    if show:
        plt.show()
    
    if save_path:
        plt.savefig(save_path)
    
