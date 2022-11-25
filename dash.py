# Import modules. Check requirements.txt for dependencies
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
from streamlit_folium import st_folium
import random as rd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from generate_wordcloud import generate_data, create_wordcloud
from shapely.geometry import Point, Polygon
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components


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

HtmlFile1 = open("christoffer/absolute funding.html", 'r', encoding='utf-8')
HtmlFile2 = open("christoffer/average_funding.html", 'r', encoding='utf-8')

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
    st_map = st_folium(map, width=800, height=450)



    


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
    
        
        maincol1, maincol2 = st.columns([20,1])
        with maincol1:
            
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
        title_col1, title_col2 = st.columns([2,3])
        with title_col1:

            with st.container():
                for i in range(2):
                    "\n"
                   
                with st.expander("Open / Collapse filters", expanded=True):
                    st.subheader("Filters")

                    locations = st.selectbox("Choose an institution", institution)

                    theme = st.selectbox("Choose a theme", omraade)

                    year = st.selectbox("Year", years)

        "---"
        
        

        multi_select = st.multiselect('Choose Average or Absolute', ['Absolute', 'Average'], default='Absolute')

        dashcol1, dashcol2 = st.columns([2,2])

        if 'Absolute' in multi_select:
                with dashcol1:
                    components.html(HtmlFile1.read(), width=650, height=500)
        if 'Average' in multi_select:
            with dashcol2:
                components.html(HtmlFile2.read(), width=650, height=500)


        with title_col2:
            with st.container():
                for i in range(2):
                    "\n"
                with st.expander("Expand for Map and Data table", expanded=True):

                    dataset = filters(locations, theme, year)
                    st.dataframe(dataset)
                    map = display_map(locations, theme)
            
        
            
            

        
            

            


                    
            

            

            


        
        
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
            
      
           
                
#### Checking for user choice and displaying context of menu ####
if choose == "Dashboard":
    dashboard()
    

if choose == "About":
    about()

    


#### ADD SUMMARY!!! ####
    


    
        

    
    









