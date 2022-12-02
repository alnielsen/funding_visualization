from christoffer.text_viz import * 
import pandas as pd
from streamlit import experimental_memo

TOP_N = 50

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
def generate_bar_chart(df, animated = False):
    """
    Wrapper function for generating frequncy bar charts
    """
    if animated:
        return create_animated_bar(df,
                                  y_col= "freqs",
                                  color_col = "avg_funding",
                                  color_label= "Average Funding pr. Grant",
                                  x_label = "Word Frequency",
                                  title = "Top 50 Most Used Words By Year")
    else:
        return create_bar_plot(df = gen_chart_data(df, top_n = TOP_N, yearly = False, sort_col = "freqs"),
                              y_col = "freqs",
                              color_col = "avg_funding",
                              title = f"Top {TOP_N} Most Used Words Across All Time (2013 - 2022)",
                              color_label = "Average Funding pr. Grant",
                              x_label = "Frequency")


#########
# Buble #
#########
@experimental_memo
def generate_bubble_chart(df, animated = False):
    """
    Wrapper function for creating bubble charts
    """
    if animated:
        return create_bubble_plot(df = gen_chart_data(df, top_n= TOP_N, yearly = True, sort_col = "funding"),
                          y_col = "funding",
                          x_col = "avg_funding",
                          size_col = "freqs",
                          color_col= "freqs",
                          y_strech = 10000000,
                          x_strech = 1000000,
                          title=f"Top {TOP_N} Most Funded Words Each Year",
                          y_lab = "Combined Funding",
                          x_lab= "Average Funding pr. Grant",
                          size_lab = "Word Frequency",
                          color_lab = "Word Frequency")
    else:
        return create_bubble_plot(df = gen_chart_data(df, top_n= TOP_N, yearly = False, sort_col = "funding"),
                                y_col = "funding",
                                x_col = "avg_funding",
                                size_col = "freqs",
                                color_col= "freqs",
                                y_strech = 50000000,
                                x_strech = 1000000,
                                title=f"Top {TOP_N} Most Funded Words Across All Years",
                                y_lab = "Combined Funding",
                                x_lab= "Average Funding pr. Grant",
                                size_lab = "Word Frequency",
                                color_lab = "Word Frequency")

@experimental_memo
def generate_bubble_words(df, words, animated = False):
    if animated:
        return create_bubble_plot(df = gen_chart_data(df, sort_col= "freqs", yearly = True, words = words),
                                y_col = "freqs",
                                x_col = "avg_funding",
                                size_col = "funding",
                                color_col= "funding",
                                y_strech = 10,
                                x_strech = 1000000,
                                title=f"Funding for Chosen words Each Year",
                                y_lab = "Number of Grants Containing Word",
                                x_lab= "Average funding pr. Grant",
                                size_lab = "Combined Funding for all Grants Containing Word",
                                color_lab = "Combined Funding for all Grants Containing Word")    
    else:
        return create_bubble_plot(df = gen_chart_data(df, sort_col= "freqs", yearly = False, words = words),
                                y_col = "freqs",
                                x_col = "avg_funding",
                                size_col = "funding",
                                color_col= "funding",
                                y_strech = 10,
                                x_strech = 1000000,
                                title=f"Funding for Chosen words Each Year",
                                y_lab = "Number of Grants Containing Word",
                                x_lab= "Average funding pr. Grant",
                                size_lab = "Combined Funding for all Grants Containing Word",
                                color_lab = "Combined Funding for all Grants Containing Word")
##########
# Graphs #
##########
@experimental_memo
def generate_graph_total(df, min_deg = 800):
    """
    Wrapper for generating a graph over total word connectivity
    """
    G = generate_graph_data(df = df, min_deg = min_deg)
    return plot_graph(G, title = "Most Interconnected Words (All Time)")

@experimental_memo
def generate_graph_year(df, year, min_deg):
    """
    Wrapper for generating of graph over word connectivity in a given year
    """
    df = df[df["År"] == year]
    G = generate_graph_data(df = df, min_deg = min_deg)
    return plot_graph(G, title = f"Most Interconnected Words ({year})")

@experimental_memo
def generate_graph_words(df, words, min_deg = 0):
    """
    Wrapper for generating a graph over connectivity between chosen words
    """
    G = generate_graph_data(df = df, words = words, min_deg = 0)
    return plot_graph(G, title = f"Connectivity Between {words}")

@experimental_memo
def generate_graph_single_word(df, word, min_deg):
    G = generate_graph_data(df = df, spec_word = word, min_deg = min_deg)
    return plot_graph(G, title = f"Connectivity For '{word}'")    



"""
All functions returns a plotly figure.
Moreover All functions expect to have the full data set we have scraped.
The functions handles all filtering internally through the parameter settings.

Examples of how to call the functions

# Data
>>> df = pd.read_csv("../gustav/dff.csv")

Word cloud where size is determiend by frequencies
>>> wordcloud_freqs = generate_wordcloud_freqs(df)

Word cloud where size is determiend by funding
>>> wordcloud = generate_wordcloud_funding(df)

# Buble chart with aggregated numbers
>>> bub_chart = generate_bubble_chart(df)

# Bubble chart with a yearly slider
>>> animated_bub = generate_bubble_chart(df, animated = True)

# Bubble chart over some chosen words
>>> my_words = ["projekt", "undersøge", "behandling", "udvikling", "data", "bedre", "første", "tool-box", "twenty", "north"]
>>> word_bub = generate_bubble_words(df, words = my_words)

# Bubble chart over same chosen words by year
>>> my_words = ["projekt", "undersøge", "behandling", "udvikling", "data", "bedre", "første", "tool-box", "twenty", "north"]
>>> word_bub_animated = generate_bubble_words(df, words = my_words, animated = True)

# Bar chart over total frequencies
>>> total_bar_chart = generate_bar_chart(df)

# Bar chart with frequencies by year
>>> yearly_bar_chart = generate_bar_chart(df, animated = True)

# Graph over total word connections
>>> graph_all_words = generate_graph_total(df, min_deg = 800)

# Graph over total word connections in a given year
>>> graph_2013 = generate_graph_year(df, year = 2013, min_deg= 80)

# Graph over Connections between chosen words
>>> my_words = ["novel", "green", "system", "transition", "study", "patients", "covid"]
>>> graph_chosen_words = generate_graph_words(df, words = my_words, min_deg = 0)

# Graph over connections for a single word
>>> my_word = "green"
>>> graph_green = generate_graph_single_word(df, word = "green", min_deg = 20) 

"""