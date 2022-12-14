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
from christoffer.generate_figs import generate_wordcloud_freqs, generate_wordcloud_funding, generate_bar_chart, generate_bubble_chart, generate_bubble_words, generate_graph_top_n, generate_graph_words, generate_graph_single_word
from christoffer.text_viz import get_all_words, generate_data
from gustav.gustav_figs import generateSankey

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

def full_screen_fix():
    style_fullscreen_button_css = """
                button[title="View fullscreen"] {
                    background-color: #004170cc;
                    right: 0;
                    color: white;
                }

                button[title="View fullscreen"]:hover {
                    background-color:  #004170;
                    color: white;
                    }
                """
    st.markdown(
        "<style>"
        + style_fullscreen_button_css
        + "</styles>",
        unsafe_allow_html=True,)


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
        
        with st.expander("Filters", expanded=True):

            locations = st.selectbox("Choose an institution", institution)
            dashtype = st.radio("Choose dashboard type", ['Investigator', 'Comparer'])

            if locations == "All":
                df = full_df
            else:
                df = full_df.loc[(full_df["Institution"] == locations)]
            

        
        with st.expander('Need instructions?'):

            st.write("How to use:")
#### Creating the dashboard section ####
st.cache()
def dashboard(df):
        
    #### INVESTIGATOR SECTION ####

    if dashtype == 'Investigator':
        maincol1, maincol2 = st.columns([2,2], gap="large")  
        with maincol1:
            st.write("Institution")
            st.subheader(f"{locations}")
            
        
        with maincol2:
            #years = df["År"]
            #years.append("All Time")
            years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, "All Time"]
            year = st.select_slider("Year",
                                    options= years,
                                    value='All Time')
                                          
            
        
            if year == "All Time":
                df = df
            if not year == "All Time":
                df = df.loc[(df["År"] == year)]
        "---"
        metriccol1, metriccol2, metriccol3, metriccol4, metriccol5, metriccol6 = st.columns([1,3,4,3,3,1], gap="medium")
        
        with metriccol2:
            st.write("Year selected:")
            st.subheader(year)
        
        with metriccol3:
            all_sum = sum(df["Bevilliget beløb"])
            st.write(f"Total funding:")
            st.subheader(f'{all_sum:,} DKK')
            
        with metriccol4:
            num_projects = len(df)
            st.write(f"Number of funded projects:")
            st.subheader(f'{num_projects}')
            
        with metriccol5:
            try:
                avg_fund = all_sum//num_projects
            except ZeroDivisionError:
                avg_fund = 0    
            st.write(f"Average funding pr. project:")
            st.subheader(f'{avg_fund:,} DKK')
        
        "---"
        
        with st.expander("Flow of funding", expanded=False):
            sankey = generateSankey(df, year=year, category_columns=['År','Virkemidler', 'Område'])
            st.plotly_chart(sankey, use_container_width=True)
            
        with st.expander("Most Frequently Used Words", expanded=False):
            top_n = st.select_slider("Top Most used words",
                        options=[i for i in range(10, 81)],
                        value = 50,
                        label_visibility= "hidden",
                        key = "top_n_bar_slider")
            barchart = generate_bar_chart(df, animated = False, top_n = top_n)
            st.plotly_chart(barchart, use_container_width=True)

        with st.expander("Most Funded Words", expanded=False):
            top_n = st.select_slider("Top Most Funded Words",
                        options=[i for i in range(10, 81)],
                        value = 50,
                        label_visibility= "hidden",
                        key = "top_n_bub_slider")
            bubchart = generate_bubble_chart(df, top_n = top_n, animated = False)
            st.plotly_chart(bubchart, use_container_width=True)

        with st.expander("Word Connections", expanded=False):
            top_n = st.select_slider("Top word connections: ",
                        options=[i for i in range(2, 81)],
                        value = 10,
                        key = "top_n_words_slider")
            graph_chart = generate_graph_top_n(df, top_n)
            st.plotly_chart(graph_chart, use_container_width=True)
        "---"
        if not len(df) == 0: 
            header_col1, header_col2 = st.columns([1, 2], gap="large")  
            st.cache()
            avg_funding, funding, freqs =  generate_data(df = df,
                                                        funding_thresh_hold = 0)
            st.cache()
            all_words = get_all_words(df)
            with header_col1:
                st.subheader(f"Word Explorer")
            with header_col2:
                selected_words = st.multiselect("Select Word:", options = all_words, default = all_words[0], )
            
            "---"
            word_col1, word_col2, word_col3, word_col4, word_col5, word_col7 = st.columns([1,3,3,3,3,1], gap="medium")
            with word_col2:
                st.write("**Selected Words:**")
                for word in selected_words:
                    st.write(f"{word}")

            with word_col3:
                st.write("**Combined Funding:**")
                for word in selected_words:
                    st.write(f"{funding[word]:,} DKK")
            with word_col4:
                st.write("**Average Funding:**")
                for word in selected_words:
                    st.write(f"{avg_funding[word]:,} DKK")   
            with word_col5:
                st.write("**Times used in Title:**")
                for word in selected_words:
                    st.write(f"{freqs[word]}")    
            "---"
            with st.expander("Explore Connectivity Between selected words", expanded=False):
                
                activate_btn = st.button("Generate Connectivty Graph", key="activate1")
                if activate_btn:
                    graph_chart = generate_graph_words(df, words= selected_words)
                    st.plotly_chart(graph_chart, use_container_width=True)
                
            with st.expander("Explore Connectivity For Selected Word", expanded=False):      
                select_word = st.selectbox("Choose Word:", options = selected_words)
                top_n_investigation = st.select_slider("Top word connections: ",
                            options=[i for i in range(2, 81)],
                            value = 10,
                            key = "word_investigation_slider")
                if select_word is not None:
                    graph_chart_single = generate_graph_single_word(df, word=select_word, top_n = top_n_investigation)
                    st.plotly_chart(graph_chart_single, use_container_width=True)   
            
            with st.expander("Explore Funding For Selected Words", expanded=False):
                words_bub_chart = generate_bubble_words(df, words = selected_words, animated=False)
                st.plotly_chart(words_bub_chart, use_container_width=True)

            with st.expander("Explore Word Frequencies"):
                barchart_words = generate_bar_chart(df, top_n = len(df) - 1, words = selected_words)
                st.plotly_chart(barchart_words, use_container_width=True)          
        full_screen_fix()
    
    if dashtype == 'Comparer':
        "hej"








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



if choose == "Dashboard":
    dashboard(df)

if choose == "About":
    about()
            
    


