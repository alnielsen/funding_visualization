from text_viz import * #create_wordcloud, plot_wc, generate_data, create_bar_plot, create_bubble_plot, gen_chart_data, create_animated_bar generate_graph_data
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
from math import inf, floor, ceil, isnan
df = pd.read_csv("../gustav/dff.csv")
avg_funding, funding, freqs = generate_data(df = df,
                                            funding_thresh_hold = 0)


###########
# Funding #
###########
TOP_N = 50
wc = create_wordcloud(size_dict = funding,
                      color_dict = freqs)
plot_wc(wordcloud = wc,
        title = "Most Funded Words (2013 - 2022)",
        show = False,
        save_path = "output/standalone/wordcloud_funding.png")

fig = create_bubble_plot(df = gen_chart_data(df, top_n= TOP_N, yearly = True, sort_col = "funding"),
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
fig.write_html("output/standalone/bubble_top_funded_words_yearly.html", auto_play = False)

fig = create_bubble_plot(df = gen_chart_data(df, top_n= TOP_N, yearly = False, sort_col = "funding"),
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
fig.write_html("output/standalone/bubble_top_funded_words_all.html", auto_play = False)


#########
# Freqs #
#########
wc = create_wordcloud(size_dict = funding,
                      color_dict = freqs)
plot_wc(wordcloud = wc,
        title = "Most Used Words Across All Time (2013 - 2022)",
        show = False,
        save_path = "output/standalone/wordcloud_freqs.png")

fig = create_bar_plot(df = gen_chart_data(df, top_n = TOP_N, yearly = False, sort_col = "freqs"),
                    y_col = "freqs",
                    color_col = "avg_funding",
                    title = f"Top {TOP_N} Most Used Words Across All Time (2013 - 2022)",
                    color_label = "Average Funding pr. Grant",
                    x_label = "Frequency")
fig.write_html(f"output/standalone/bar_top_freqs_words_all_years.html", auto_play = False)   

fig = create_animated_bar(df, y_col= "freqs",
                          color_col = "avg_funding",
                          color_label= "Average Funding pr. Grant",
                          x_label = "Word Frequency",
                          title = "Top 50 Most Used Words By Year")

fig.write_html("output/standalone/bar_top_freqs_words_yearly.html", auto_play = False)



"""

words = ["projekt", "undersøge", "behandling", "udvikling", "data", "bedre", "første", "tool-box", "twenty", "north"]
words_df = gen_chart_data(df, words = words)
fig = create_bubble_plot(df = words_df,
                          y_col = "freqs",
                          x_col = "avg_funding",
                          size_col = "funding",
                          color_col= "funding",
                          y_strech = 50,
                          x_strech = 1000000,
                          title=f"Funding for Chosen words Each Year",
                          y_lab = "Number of Grants Containing Word",
                          x_lab= "Average funding pr. Grant",
                          size_lab = "Combined Funding for all Grants Containing Word",
                          color_lab = "Combined Funding for all Grants Containing Word")
fig.write_html("output/bubble_test_specific_words.html", auto_play = False)
"""


##########
# Graphs #
##########
df = pd.read_csv("../gustav/dff.csv")
G = generate_graph_data(df, min_deg = 800)
fig = plot_graph(G, title = "Most Interconnected Words (All Time)")
fig.write_html("output/standalone/Graf all Time.html")

years = list(set(df["År"]))

for year in years:
    print(year)
    temp_df = df[df["År"] == year]
    G = generate_graph_data(temp_df, min_deg = 80)
    fig = plot_graph(G,
                     title = f"Most Interconnected Words ({year})")
    fig.write_html(f"output/standalone/graph each year/Graf {year}.html")
