# Import Libraries. Check requirements.txt for dependencies

## STREAMLIT LIBRARIES ##
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from st_aggrid import AgGrid

## DATAFRAMES LIBRRIES ##
import pandas as pd
import geopandas as gpd

## MAP LIBRARIES ##
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from streamlit_folium import st_folium

## PLOT AND GEOMETRY LIBRARIES
import plotly.express as px
import plotly.graph_objects as go
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
import random as rd

## CUSTOM LIBRARIES ##
from christoffer.text_viz import generate_data, gen_bubble_data, create_bar_plot, create_bubble_plot, create_wordcloud

# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state="collapsed")


## Load dataset
df = pd.read_csv('gustav/dff.csv')

institution = ['All']

for i in df['Institution']:
    if i not in institution:
        institution.append(i)


omraade = ['All']

for i in df['Område']:
     if i not in omraade:
        omraade.append(i)


amount = []

for i in df["Bevilliget beløb"]:
    if i not in amount:
        amount.append(i)
#amount.insert(0,'All')


years = []

for i in range(2013, 2023):
    if i not in years:
        years.append(i)
years.sort(reverse=True)
years.insert(0, 'All')


## Filter function / Display filters ##
@st.experimental_memo
def filters(institution, tema, år):
    locations = institution
    theme = tema
    year = år

    ## No filtering
    if locations == 'All' and theme == 'All' and year == 'All':
        data = df
        return data

    ## Filter for year
    elif locations == 'All' and theme == 'All' and year == year:
        data = df.loc[(df["År"] == year)]
        return data

    ## Filter for theme
    elif locations == 'All' and theme == theme and year == 'All':
        data = (df.loc[(df["Område"] == theme)])
        return data

    ## Filter for location
    elif locations == locations and theme == 'All' and year == 'All':
        data = df.loc[(df["Institution"] == locations)]
        return data

    ## Filter for theme and year
    elif locations == 'All' and theme == theme and year == year:
        data = df.loc[(df["Område"] == theme) & (df["År"] == year)]
        return data
    
    ## Filter for location and theme
    elif locations == locations and theme == theme and year == 'All':
        data = df.loc[(df["Institution"] == locations) & (df["Område"] == theme)]
        return data

    ## Filter for location and year
    elif locations == locations and theme == 'All' and year == year:
        data = df.loc[(df["Institution"] == locations) & (df["År"] == year)]
        return data

    ## Filter for all
    elif locations == locations and theme == theme and year == year:
        data = df.loc[(df["Institution"] == locations) & (df["Område"] == theme) & df["År"] == year]
        return data


## Generate bar plots ##
@st.experimental_memo
def gen_bar_plots():

    avg_funding, funding, freqs = generate_data(df = df,
                                            funding_thresh_hold = 0)
#############
# Bar plots #
#############
    TOP_N = 30



    fig_funding = create_bar_plot(data_dict = funding,
                                color_dict = freqs,
                                color_label = "# of Grants Containing Word",
                                value_label = "Funding across all grants",
                                title = f"Top {TOP_N} words with highest funding ",
                                top_n = TOP_N)
    return fig_funding


## Generate sankey chart ##
@st.experimental_memo
def generateSankey(df, year, category_columns):
    df.tail()

    colorpalette = px.colors.qualitative.Plotly

    # data for sankey
    df = df.loc[df['År'] == year]
    df_sankey = df.loc[:,category_columns + ['Bevilliget beløb']]

    # create list of labels, i.e. unique values from each column except the values
    # create color list
    labels = []
    colornumlist = []

    for col in category_columns:
        labels = labels + list(set(df_sankey[col].values)) # adds unique labels in each category to list
        colornumlist.append(len(list(set(df_sankey[col].values)))) # appends number of unique labels for each category

    # define colors based on number of categories
    colorList = []
    for idx, colorNum in enumerate(colornumlist):
        colorList = colorList + [colorpalette[idx]]*colorNum

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
            color = colorList
            ),
        link = dict(
            source = df_link_input['sourceID'], # indices correspond to labels, e.g. '2022', 'Forskningsprojekt 1', 'Forskningsprojekt 2', ...
            target = df_link_input['targetID'],
            value = df_link_input['count']
        ))])

    fig.update_layout(title_text="Funding of Research Grants in " + str(year) + "<br>Source: <a href='https://dff.dk/'>Danmarks Frie Forskningsfond</a>",
                        font_size=10)
    return fig


## Generate wordcloud ##
@st.experimental_memo
def gen_wordcloud():
    avg_funding, funding, freqs = generate_data(df = df,
                                            funding_thresh_hold = 0)
    
    wc = create_wordcloud(size_dict=funding, color_dict=freqs)

    return wc
    

## Generate and display map ##
def display_map(institution, tema):

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    location = geolocator.geocode(institution)

    lat = location.latitude
    lon = location.longitude

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    tooltip = 'Show info.'
    
    map = folium.Map(location=map_data, zoom_start=10, scrollWheelZoom=False, width='100%', height="100%")
    folium.Marker(
    [lat, lon], popup=f'{institution}', tooltip=tooltip
    ).add_to(map)
    return map


#### Histogram function ####
def histo_chart():
    
    fig = px.histogram(df, x="Bevilliget beløb",
                   title='Histogram of grants',
                   nbins=30,
                   #histnorm='percent',
                   color_discrete_sequence=['indianred'] # color of histogram bars
                   )
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)


streamlit_style = """

			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;

			}
			</style>
			"""

st.markdown(streamlit_style, unsafe_allow_html=True)


# Markdown code to hide "hamburger-menu"
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True,)


#### Configuring Sidebar/Navigation bar ####
with st.sidebar:
    choose = option_menu("Navigation bar", ["Dashboard", "About"],
                         icons=['speedometer', 'question-square'],
                         menu_icon="segmented-nav", default_index=0,
                         styles={
                                "container": {"padding": "5!important", "background-color": "#435870"},
                                "icon": {"color": "orange", "font-size": "20px"}, 
                                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#b7bcc4"},
                                "nav-link-selected": {"background-color": "#313945"},
                                }, orientation='horizontal')






#### Creating the dashboard section ####
st.cache()
def dashboard():
    top_col1,top_col2,top_col3 = st.columns([2,2,2], gap="large")
    
    with top_col1:
        with st.container():

            st.markdown("""
            <style>
            .big-font {
                font-size:18px !important;
            }
            </style>
            """, unsafe_allow_html=True)

            ## Section description ##
            st.header("Danmarks Frie Forskningsfond")
            st.markdown('<p class="big-font">Visualization of funding data & funding flows</p>', unsafe_allow_html=True)

    with top_col2:
        with st.container():
            with st.expander("Open/Close Filters", expanded=True):

                locations = st.selectbox("Choose an institution", institution)

                theme = st.selectbox("Choose a theme", omraade)

                year = st.selectbox("Year", years)

    with top_col3:
        with st.container():
            with st.expander('Need instructions?'):
                st.write("How to use:")

    ("---")

    for break_page in range(2):
        st.write("\n")
    

    sankeycol1,sankeycol2,sankeycol3 = st.columns([1,7,1])

    with sankeycol2:
        with st.container():
            with st.expander("Display Sankey chart", expanded=True):
                    # NODES UDE TIL HØJRE SKAL SORTERES I FALDENDE ORDEN
                    # plotting sankey diagram
                    year_slider = st.slider("Year", min_value=2013, max_value=2022, value=2013)
                    sankey = generateSankey(df, year=year_slider, category_columns = ['År','Virkemidler', 'Område'])
                    st.plotly_chart(sankey, use_container_width=True)

    for break_page in range(2):
        st.write("\n")

    barcol1, barcol2, barcol3 = st.columns([1,7,1])

    with barcol2:
        with st.container():
            ## Display bar plots ##
            with st.expander("Absolute Funding", expanded=False):
                fig1 = gen_bar_plots()
                st.plotly_chart(fig1, use_container_width=True)

    
    for break_page in range(2):
        st.write("\n")


    cloudcol1, cloudcol2, cloudcol3 = st.columns([5,2,5])

    with cloudcol2:
        with st.container():
            ## Display Wordcloud ##
            with st.expander("Wordcloud for funding", expanded=False):
                    fig2 = gen_wordcloud()
                    st.image(fig2.to_array())

    for break_page in range(2):
        st.write("\n")


    datacol1,datacol2,datacol3 = st.columns([1,7,1])

    with datacol2:
        with st.container():
            with st.expander("Expand for Data table", expanded=False):

                dataset = filters(locations, theme, year)
                st.dataframe(dataset)
            

    
#### Creating the About section ####

def about():
    
    source = 'All data is soruced from: [Danmarks Frie Forskningsfond](https://dff.dk/forskningsprojekter)'
    
    st.title("About the Visualizer")
    ("How do i use the visualizer and what can it tell me?")

    st.markdown("***")

    st.title("About the Data")
    
    st.markdown(source, unsafe_allow_html=True)
    ("Data holds information about funds, institutions, themes and more.")
    for i in range(3):
        st.write('\n')
    ("You can download the data in .csv format below")

    with open ("gustav/dff.csv", "rb") as file:
        btn = st.download_button(
            label="Download Data",
            data=file,
            file_name="dff_data.csv",
            mime="text/csv"
          )
    "---"
    #st.dataframe(df)

    ## Add creator as expander with info with git links ##
    with st.sidebar:
        
        with st.expander("Creators"):
                  
            # Add Link to your repo
            aln_git = '''
            [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/alnielsen) 

            '''
            gc_git = '''

            [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/gustavchristensen1995) 

            '''
            cmk_git = '''
            [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/Chris-Kramer) 

            '''
            
            ("Andreas LN")
            (aln_git)
            st.markdown("***")
            ("Christoffer M.K.")
            (cmk_git)
            st.markdown("***")
            ("Gustav C.")
            (gc_git)
            st.markdown("***")




#### Checking for user navigation choice and displaying context of menu ####
if choose == "Dashboard":
    dashboard()

if choose == "About":
    about()


    