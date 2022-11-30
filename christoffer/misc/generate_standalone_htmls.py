import pandas as pd
from generate_figs import *


df = pd.read_csv("../../gustav/dff.csv")
###############
# Word clouds #
###############
plot_wc(wordcloud = generate_wordcloud_freqs(df),
        title = "Most Funded Words (2013 - 2022)",
        show = False,
        save_path = "../output/standalone/wordcloud_funding.png")

plot_wc(wordcloud = generate_wordcloud_funding(df),
        title = "Most Used Words Across All Time (2013 - 2022)",
        show = False,
        save_path = "../output/standalone/wordcloud_freqs.png")

#################
# Bubble charts #
#################
fig = generate_bubble_chart(df, animated = True)
fig.write_html("../output/standalone/bubble_top_funded_words_yearly.html", auto_play = False)

fig = generate_bubble_chart(df)
fig.write_html("../output/standalone/bubble_top_funded_words_all.html", auto_play = False)


words = ["projekt", "undersøge", "behandling", "udvikling", "data", "bedre", "første", "tool-box", "twenty", "north"]
fig = generate_bubble_words(df, words = words, animated = False)
fig.write_html("../output/test/bubble_test_specific_words.html", auto_play = False)

fig = generate_bubble_words(df, words = words, animated = True)
fig.write_html("../output/test/bubble_test_specific_words_yearly.html", auto_play = False)


#########
# Freqs #
#########
fig = generate_bar_chart(df)
fig.write_html(f"../output/standalone/bar_top_freqs_words_all_years.html", auto_play = False)   

fig = generate_bar_chart(df, animated = True)
fig.write_html("../output/standalone/bar_top_freqs_words_yearly.html", auto_play = False)

##########
# Graphs #
##########
fig = generate_graph_total(df, min_deg = 800)
fig.write_html("../output/standalone/Graf all Time.html")

years = list(set(df["År"]))
for year in years:
    fig =generate_graph_year(df, year = year, min_deg= 80)
    fig.write_html(f"../output/standalone/graph each year/Graf {year}.html")

words = ["novel", "green", "system", "transition", "study", "patients", "covid"]
fig = generate_graph_words(df, words = words, min_deg = 0)
fig.write_html("../output/test/graf spec words.html")


fig = generate_graph_single_word(df, word = "green", min_deg = 20)
fig.write_html("../output/test/graf green.html")