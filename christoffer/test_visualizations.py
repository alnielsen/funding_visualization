from text_viz import create_wordcloud, plot_wc, generate_data, create_bar_plot
import plotly.express as px
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

dataframe = pd.read_csv("../gustav/dff.csv")
dataframe = dataframe[dataframe["År"] == 2013]
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
