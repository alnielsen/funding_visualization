from text_viz import create_wordcloud, plot_wc, generate_data, create_bar_plot, create_bubble_plot, gen_spec_w_bub_data, gen_top_bub_data
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



"""
Example wordclouds -- How to use
>>> dataframe = pd.read_csv("../gustav/dff.csv")
>>> funding_thresh = 50000
>>> funding, freqs = generate_data(df = dataframe,
                                   funding_thresh_hold = funding_thresh)
>>> w_cloud = create_wordcloud(size_dict = funding,
                               color_dict = freqs)
"""
"""
dataframe = pd.read_csv("../gustav/dff.csv")
avg_funding, funding, freqs = generate_data(df = dataframe,
                                            funding_thresh_hold = 0)


# Bar plots
TOP_N = 30
fig_avg = create_bar_plot(data_dict = avg_funding, 
                          color_dict = freqs,
                          color_label = "Grants Containing Word",
                          value_label = "Average Funding pr. Grant",
                          title = f"Top {TOP_N} words with highest average funding",
                          top_n = TOP_N)
fig_avg.write_html("average_funding.html")

fig_funding = create_bar_plot(data_dict = funding,
                              color_dict = freqs,
                              color_label = "# of Grants Containing Word",
                              value_label = "Funding across all grants",
                              title = f"Top {TOP_N} words with highest funding ",
                              top_n = TOP_N)
fig_funding.write_html("absolute funding.html")
"""
"""
df = pd.read_csv("../gustav/dff.csv")
years = list(set(df["År"]))
years.sort()
df_dict = {"word": [], "freqs": [], "funding": [], "avg_funding": [], "year": []}
words = ["projekt", "nye", "forskellige", "novel", "new", "role"]
for year in years:
    temp_df = df[df["År"] == year]
    avg_funding, funding, freqs = generate_data(df = temp_df,
                                                funding_thresh_hold = 0)
    #for word in words:
        #word = word.lower()
    for key in funding:
        #if key == word:
        df_dict["word"].append(key)
        df_dict["freqs"].append(freqs[key])
        df_dict["funding"].append(funding[key])
        df_dict["avg_funding"].append(avg_funding[key])
        df_dict["year"].append(year)
        
df = pd.DataFrame(df_dict)
#fig = go.Figure()
fig = px.scatter(df, x="year", y="funding",
	                size="freqs", color="word",
                    hover_name="word", size_max=100)#.update_traces(mode='markers',name='Markers and Text', text = df["word"])
"""

df = pd.read_csv("../gustav/dff.csv")
TOP_N = 25
top_funded_df = gen_top_bub_data(df, TOP_N, sort_col = "funding") # The the top 25 words with highes absolute funding
fig = create_bubble_plot(df = top_funded_df,
                          y_col = "freqs",
                          x_col = "avg_funding",
                          size_col = "funding",
                          color_col= "funding",
                          y_strech = 50,
                          x_strech = 1000000,
                          title=f"Funding for {TOP_N} most funded words each year",
                          y_lab = "Number of Grants Containing Word",
                          x_lab= "Average funding pr. Grant",
                          size_lab = "Combined Funding for all Grants Containing Word",
                          color_lab = "Combined Funding for all Grants Containing Word")
fig.write_html("bubble_top_funded_words.html", auto_play = False)

words = ["projekt", "undersøge", "behandling", "udvikling", "data", "bedre", "første", "tool-box", "twenty", "north"]
words_df = gen_spec_w_bub_data(df, words)
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
fig.write_html("bubble_test_specific_words.html", auto_play = False)