from text_viz import create_wordcloud, plot_wc, generate_data, dict_to_df, create_bar_plot
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
"""
# Bar plots
TOP_N = 50
fig_avg = create_bar_plot(avg_funding, 
                          value_label = "Funding divided by frequency",
                          title = f"Top {TOP_N} words with highest average funding",
                          top_n = TOP_N)
fig_avg.show()

fig_funding = create_bar_plot(funding,
                              value_label = "Funding across all grants",
                              title = f"Top {TOP_N} words with highest funding ",
                              top_n = TOP_N)
fig_funding.show()

fig_freqs = create_bar_plot(freqs,
                            value_label = "Grant frequency",
                            title = f"Top {TOP_N} most used words in different grants",
                            top_n = TOP_N)
fig_freqs.show()
"""

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
