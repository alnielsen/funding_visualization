from christoffer.text_viz import *
#from text_viz import *
import pandas as pd
from streamlit import experimental_memo

###############
# Word clouds #
###############
@experimental_memo
def generate_wordcloud_freqs(df):
    avg_funding, funding, freqs = generate_data(df = df,
                                                funding_thresh_hold = 0)
    return create_wordcloud(size_dict = funding,
                            color_dict = freqs)

@experimental_memo
def generate_wordcloud_funding(df):
    avg_funding, funding, freqs = generate_data(df = df,
                                                funding_thresh_hold = 0)
    return create_wordcloud(size_dict = funding,
                            color_dict = freqs)


#############
# Bar plots #
#############
@experimental_memo
def generate_bar_chart(df, top_n = None, animated = False, words = None):
    """
    Wrapper function for generating frequncy bar charts
    """
    if animated:
        return create_animated_bar(df,
                                  x_col= "freqs",
                                  color_col = "avg_funding",
                                  color_label= "Average Funding pr. Grant",
                                  x_label = "Word Frequency",
                                  top_n = top_n,
                                  title = "Top {top_n} Most Used Words By Year")
    elif words is None:
        return create_bar_plot(df = gen_chart_data(df, top_n = top_n, yearly = False, sort_col = "funding"),
                              x_col = "freqs",
                              color_col = "avg_funding",
                              title = f" ",
                              color_label = "Average Funding pr. Grant",
                              x_label = "Frequency")
    elif words is not None:
        return create_bar_plot(df = gen_chart_data(df, yearly = False, sort_col = "funding", words=words),
                               x_col = "freqs",
                               color_col = "avg_funding",
                               title = f" ",
                               color_label = "Average Funding pr. Grant",
                               x_label = "Frequency")


#########
# Buble #
#########
X_STRETCH = 0.1
Y_STRETCH = 0.1
@experimental_memo
def generate_bubble_chart(df, top_n = 50, animated = False):
    """
    Wrapper function for creating bubble charts
    """

    if animated:
        return create_bubble_plot(df = gen_chart_data(df, top_n= top_n, yearly = True, sort_col = "funding"),
                          y_col = "funding",
                          x_col = "avg_funding",
                          size_col = "freqs",
                          color_col= "freqs",
                          y_strech = Y_STRETCH,
                          x_strech = X_STRETCH,
                          title=f"Top {top_n} Most Funded Words Each Year",
                          y_lab = "Combined Funding",
                          x_lab= "Average Funding pr. Grant",
                          size_lab = "Word Frequency",
                          color_lab = "Word Frequency")
    else:
        return create_bubble_plot(df = gen_chart_data(df, top_n = top_n, yearly = False, sort_col = "funding"),
                                y_col = "funding",
                                x_col = "avg_funding",
                                size_col = "freqs",
                                color_col= "freqs",
                                y_strech = Y_STRETCH,
                                x_strech = X_STRETCH,
                                title=f" ",
                                y_lab = "Combined Funding",
                                x_lab= "Average Funding pr. Grant",
                                size_lab = "Word Frequency",
                                color_lab = "Word Frequency")

@experimental_memo
def generate_bubble_words(df, words, animated = False):
    if animated:
        return create_bubble_plot(df = gen_chart_data(df, sort_col= "freqs", yearly = True, words = words),
                                y_col = "funding",
                                x_col = "avg_funding",
                                size_col = "freqs",
                                color_col= "freqs",
                                y_strech = Y_STRETCH,
                                x_strech = X_STRETCH,
                                title=f"Funding for Chosen words Each Year",
                                y_lab = "Number of Grants Containing Word",
                                x_lab= "Average funding pr. Grant",
                                size_lab = "Combined Funding for all Grants Containing Word",
                                color_lab = "Combined Funding for all Grants Containing Word")    
    else:
        return create_bubble_plot(df = gen_chart_data(df, sort_col= "funding", yearly = False, words = words),
                                y_col = "funding",
                                x_col = "avg_funding",
                                size_col = "freqs",
                                color_col= "freqs",
                                y_strech = Y_STRETCH,
                                x_strech = X_STRETCH,
                                title=f" ",
                                y_lab = "Combined Funding",
                                x_lab= "Average funding pr. Grant",
                                size_lab = "Frequency",
                                color_lab = "Frequency")
##########
# Graphs #
##########
@experimental_memo
def generate_graph_top_n(df, top_n = 10):
    """
    Wrapper for generating a graph over total word connectivity in a dataframe
    """
    G = generate_graph_data_all(df = df, top_n = top_n)
    return plot_graph(G, title = f" ")

@experimental_memo
def generate_graph_words(df, words):
    """
    Wrapper for generating a graph over connectivity between chosen words
    """
    G = generate_graph_data_words(df = df, words = words)
    return plot_graph(G, title = f" ")

@experimental_memo
def generate_graph_single_word(df, word, top_n):
    """
    Wrapper for generating a graph over connectivity for a chosen word
    """
    G = generate_graph_data_word(df = df, word = word, top_n = top_n)
    return plot_graph(G, title = f" ")    
