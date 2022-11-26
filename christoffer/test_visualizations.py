from text_viz import create_wordcloud, plot_wc, generate_data, create_bar_plot
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
years = list(set(df["År"]))
years.sort()
df_dict = {"word": [], "freqs": [], "funding": [], "avg_funding": [], "year": []}
for year in years:
    temp_df = df[df["År"] == year]
    avg_funding, funding, freqs = generate_data(df = temp_df,
                                                funding_thresh_hold = 0)
    for key in funding: 
        df_dict["word"].append(key)
        df_dict["freqs"].append(freqs[key])
        df_dict["funding"].append(funding[key])
        df_dict["avg_funding"].append(avg_funding[key])
        df_dict["year"].append(year)

df = pd.DataFrame(df_dict)
top_n = 25
sorted_df = pd.DataFrame(columns = ["word", "freqs", "funding", "avg_funding", "year"])
for year in years:
    temp_df = df[df["year"] == year]
    temp_df = temp_df.sort_values(by="funding", ascending = False)
    temp_df = temp_df.head(top_n)
    sorted_df = pd.concat([sorted_df, temp_df], ignore_index = True)

sorted_df = sorted_df.sort_values(by="year")

sizes = list(sorted_df["funding"])
fig = px.scatter(sorted_df,
                x="freqs",
                y="avg_funding",
                animation_frame="year",
                animation_group = "word",
                size = list(sorted_df["funding"]),
                color="word",
                hover_name="word",
                size_max = 100,
                text = "word",
                title = f"Evolution of {top_n} most funded words",
                range_x=[min(df["freqs"]), max(df["freqs"]) + 25],
                range_y=[min(df["avg_funding"]), max(df["avg_funding"])]
                )
#fig["layout"].pop("updatemenus") # Remove buttons (it does not work when animating)
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 15000
fig.update_traces(textposition='middle center')
fig.write_html("bubble_test.html", auto_play = False)

fig = px.scatter(sorted_df,
                y="funding",
                x="avg_funding",
                animation_frame="year",
                animation_group = "word",
                size = list(sorted_df["freqs"]),
                color="word",
                hover_name="word",
                size_max = 100,
                text = "word",
                title = f"Evolution of {top_n} most funded words",
                range_x=[min(df["avg_funding"]), max(df["avg_funding"])],
                range_y= [min(df["funding"]), max(df["funding"]) + 25]
                )
#fig["layout"].pop("updatemenus") # Remove buttons (it does not work when animating)
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1500
fig.write_html("bubble_test_2.html", auto_play = False)
"""
# Word clouds
w_cloud_fund = create_wordcloud(size_dict = funding,
                           color_dict = freqs)

w_cloud_avg = create_wordcloud(
                           size_dict = avg_funding,
                           color_dict = funding)

w_cloud_freq = create_wordcloud(
                           size_dict = freqs,
                           color_dict = freqs)

plot_wc(w_cloud_fund, title = "Size = Funding, color = freqs")
plot_wc(w_cloud_avg, title = "Size = Avg funding, color = freqs")
plot_wc(w_cloud_freq, title = "Size = freqs, color = freqs")
"""
