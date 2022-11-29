from text_viz import create_wordcloud, plot_wc, generate_data, create_bar_plot, create_bubble_plot, gen_bubble_data, generate_graph_data
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx


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

#############
# Bar plots #
#############
TOP_N = 30
fig_avg = create_bar_plot(data_dict = avg_funding, 
                          color_dict = freqs,
                          color_label = "Grants Containing Word",
                          value_label = "Average Funding pr. Grant",
                          title = f"Top {TOP_N} words with highest average funding",
                          top_n = TOP_N)
fig_avg.write_html("output/average_funding.html")

fig_funding = create_bar_plot(data_dict = funding,
                              color_dict = freqs,
                              color_label = "# of Grants Containing Word",
                              value_label = "Funding across all grants",
                              title = f"Top {TOP_N} words with highest funding ",
                              top_n = TOP_N)
fig_funding.write_html("output/absolute funding.html")

###############
# Word clouds #
###############
wc = create_wordcloud(size_dict = funding,
                      color_dict = freqs)
plot_wc(wordcloud = wc,
        title = "Test word cloud",
        show = True,
        save_path = "output/wordcloud_test.png")

#################
# Bubble charts #
#################
df = pd.read_csv("../gustav/dff.csv")
TOP_N = 200
top_funded_df = gen_bubble_data(df,
                                top_n= TOP_N,
                                sort_col = "funding") # The the top 25 words with highes absolute funding

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
fig.write_html("output/bubble_top_funded_words.html", auto_play = False)

words = ["projekt", "undersøge", "behandling", "udvikling", "data", "bedre", "første", "tool-box", "twenty", "north"]
words_df = gen_bubble_data(df, words = words)
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
df = pd.read_csv("../gustav/dff.csv")
G = generate_graph_data(df)

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size= 10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

node_trace.marker.color =  [val for _, val in nx.get_node_attributes(G, "avg_funding").items()]
node_trace.text = [node for node in G.nodes()]
#node_trace.marker.size = [val for _, val in nx.get_node_attributes(G, "freqs").items()]

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()
fig.write_html("test.html")