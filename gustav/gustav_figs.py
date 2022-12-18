# libraries
import plotly
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import ImageColor

warnings.simplefilter(action='ignore', category=FutureWarning) # ignores warnings from pd.append()

# function to generate sankey diagram 
def generateSankey(df, year, category_columns):

    colorpalette = px.colors.qualitative.Dark24 + px.colors.qualitative.Light24 # hex values
    opacity = 0.5

    # data for sankey
    df_sankey = df.loc[:,category_columns + ['Bevilliget beløb']]

    # create list of labels, i.e. unique values from each column except the values
    labels = []

    for col in category_columns:
        labels = labels + list(set(df_sankey[col].values)) # adds unique labels in each category to list

    # define colors based on number of labels
    color_dict_labels = dict(zip(labels, colorpalette)) # zips labels list with colorpalette

    # initiate input for for loop
    df_link_input = pd.DataFrame({'source' : [], 'target': [], 'count': []})

    # create data for go.Sankey function
    for i in range(len(category_columns)-1):
        if len(category_columns) == 1:
            print("Number of input categories must be at least 2")
        else:
            temporary_df = df_sankey.groupby([category_columns[i], category_columns[i+1]]).agg({'Bevilliget beløb':'sum'}).reset_index() # loop over columns and group by column to the right, i.e. 'År' and 'Virkemidler', and then 'Virkemidler' and 'Område'
            temporary_df.columns = ['source','target','count']
            df_link_input = df_link_input.append(temporary_df)

    # add index for source-target pair
    df_link_input['sourceID'] = df_link_input['source'].apply(lambda x: labels.index(x))
    df_link_input['targetID'] = df_link_input['target'].apply(lambda x: labels.index(x))

    # define colors based on source
    colorlist_source = [color_dict_labels[i] for i in df_link_input['source']] # loops over source column, and finds the value in the dictionary, and appends it to a new list. For example, the first 8 sources are 2022, so we append the value paired with our key, i.e. 2022.
    colorlist_source_rgba = ["rgba" + str(ImageColor.getcolor(color, "RGB") + (opacity, )) for color in colorlist_source] # converts hex colors to rgba

    # creating the sankey diagram
    fig = go.Figure(data=[go.Sankey(
        valueformat = ",",
        valuesuffix = " kr.",
        # define nodes
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = list(color_dict_labels.values())
            ),
        link = dict(
            source = df_link_input['sourceID'], # indices correspond to labels, e.g. '2022', 'Forskningsprojekt 1', 'Forskningsprojekt 2', ...
            target = df_link_input['targetID'],
            value = df_link_input['count'],
            color = colorlist_source_rgba
        ))])

    fig.update_layout(title_text="Funding of Research Grants in " + str(year) + "<br>Source: <a href='https://dff.dk/'>Danmarks Frie Forskningsfond</a>",
                        font_size=10, height = 1000, width = 800)
    return fig


# stacked area chart
def generateStacked(df, y_funding, color_group):
    df_stacked = df.groupby(['År', color_group]).agg({y_funding:'sum'}).reset_index()
    fig = px.area(df_stacked, x="År", y=y_funding, color=color_group)
    fig.update_layout(
        height = 1000,
        width = 800,
        xaxis = dict(
        tickmode = 'linear',
        dtick = 1))
    
    return fig