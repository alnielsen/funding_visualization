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

streamlit_style = """

			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;

			}
			</style>
			"""

st.markdown(streamlit_style, unsafe_allow_html=True)


df = pd.read_csv('gustav/dff.csv')

avg_funding, funding, freqs = generate_data(df = df,
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



fig_funding = create_bar_plot(data_dict = funding,
                              color_dict = freqs,
                              color_label = "# of Grants Containing Word",
                              value_label = "Funding across all grants",
                              title = f"Top {TOP_N} words with highest funding ",
                              top_n = TOP_N)

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


def display_map(institution, tema):

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    location = geolocator.geocode(institution)

    lat = location.latitude
    lon = location.longitude

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    tooltip = 'Show info.'
    
    map = folium.Map(location=map_data, zoom_start=12)
    folium.Marker(
    [lat, lon], popup=f'{institution}', tooltip=tooltip
    ).add_to(map)
    st_map = st_folium(map, width=920, height=350)




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



#### Creating the dashboard section ####
def dashboard():
    
        
        maincol1, maincol2, maincol3 = st.columns([1,5,1])
        with maincol2:
            
            with st.container():

                st.markdown("""
                <style>
                .big-font {
                    font-size:20px !important;
                }
                </style>
                """, unsafe_allow_html=True)

                ## Section description ##
                st.title("Danmarks Frie Forskningsfond")
                st.markdown('<p class="big-font">Visualization of funding data & funding flows</p>', unsafe_allow_html=True)

            '---'

        filter_col1, filter_col2, filter_col3 = st.columns([2,5,2])
        with filter_col2:

            with st.container():
                   
                
                st.subheader("Filters")

                locations = st.selectbox("Choose an institution", institution)

                theme = st.selectbox("Choose a theme", omraade)

                year = st.selectbox("Year", years)
        
        with filter_col2:
            with st.container():
                map = display_map(locations, theme)


        "---"
        
        multi_select = st.multiselect('Choose Average or Absolute', ['Absolute', 'Average'], default='Absolute')

        dashcol1, dashcol2 = st.columns([1,1])

        if 'Absolute' in multi_select:
            with dashcol1:
                with st.expander("Absolute Funding", expanded=True):
                    st.plotly_chart(fig_funding, use_container_width=True)
                    
        if 'Average' in multi_select:
            with dashcol2:
                with st.expander("Average Funding", expanded=True):
                    st.plotly_chart(fig_avg, use_container_width=True)


        
        with st.container():
            for i in range(2):
                "\n"
            with st.expander("Expand for Map and Data table", expanded=True):

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
    st.dataframe(df)

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

    



    
        

    
    









