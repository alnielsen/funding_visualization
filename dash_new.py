# Import Libraries. Check requirements.txt for dependencies

## STREAMLIT LIBRARIES ##
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from st_aggrid import AgGrid
import extra_streamlit_components as stx

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
from christoffer.generate_figs import generate_wordcloud_freqs, generate_wordcloud_funding, generate_bar_chart, generate_bubble_chart, generate_bubble_words, generate_graph_total, generate_graph_year, generate_graph_words, generate_graph_single_word


# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state="expanded")


## Styling
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

## Load dataset
full_df = pd.read_csv('gustav/dff.csv', index_col=False)

## Fetch data
institution = ['All']

for i in full_df['Institution']:
    if i not in institution:
        institution.append(i)


omraade = ['All']

for i in full_df['Område']:
     if i not in omraade:
        omraade.append(i)


amount = []

for i in full_df["Bevilliget beløb"]:
    if i not in amount:
        amount.append(i)
#amount.insert(0,'All')



#### Configuring Sidebar/Navigation bar ####

with st.sidebar:
    st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)
   
    st.image("logo.png", use_column_width="auto")
    #st.markdown("<h1 style='text-align: center; color: white;'>DFF Funding Visualizer</h1>", unsafe_allow_html=True)
    choose = option_menu("", ["Dashboard", "About"],
                         icons=['speedometer', 'question-square'],
                         menu_icon="segmented-nav", default_index=0,
                         styles={
                                "container": {"padding": "5!important", "background-color": "#004c6c"},
                                "icon": {"color": "orange", "font-size": "15px"}, 
                                "nav-link": {"font-size": "13px", "text-align": "left", "margin":"5px", "--hover-color": "#eb6d7f"},
                                "nav-link-selected": {"background-color": "#007aaf"},
                                }, orientation='horizontal')
    with st.sidebar:
        with st.container():
            with st.expander("Filters", expanded=True):

                locations = st.selectbox("Choose an institution", institution)

                #theme = st.selectbox("Choose a theme", omraade)

                #year = st.selectbox("Year", years)

                #charts = st.multiselect("Choose visualizers", ['Funding flow', 'Top funded words', 'Funding wordcloud'], default="Funding flow")
                
                dashtype = st.radio("Choose dashboard type", ['Investigator', 'Comparer'])

                if locations == "All":
                    df = full_df
                else:
                    df = full_df.loc[(full_df["Institution"] == locations)]
                

            with st.container():
                with st.expander('Need instructions?'):
 
                    st.write("How to use:")
#### Creating the dashboard section ####
st.cache()
def dashboard(df):
    #### INVESTIGATOR SECTION ####
    if dashtype == 'Investigator':
        maincol1, maincol2 = st.columns([2,4])  
        with maincol1:
            st.write("Institution")
            st.subheader(f"{locations}")
            "---"

            year = st.select_slider("Year",
                                    options=[2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,"All Time"],
                                    value='All Time')
            "---"                                    

           
            if year == "All Time":
                df = df
            if not year == "All Time":
                df = df.loc[(df["År"] == year)]

            all_sum = sum(df["Bevilliget beløb"])
            st.write(f"Total funding: {year}")
            st.subheader(f'{all_sum:,} DKK')
            "---"

            num_projects = len(df)
            st.write(f"Number of funded projects: {year}")
            st.subheader(f'{num_projects}')
            "---"

            avg_fund = all_sum//num_projects
            st.write(f"Average funding pr. project: {year}")
            st.subheader(f'{avg_fund:,} DKK')
            "---"





















            
if choose == "Dashboard":
    dashboard(df)
            
    


