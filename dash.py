# Import modules. Check requirements.txt for dependencies
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io
import pydeck as pdk
from streamlit_folium import st_folium
import folium

# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state="auto")

years = [x for x in range(1900,2023)]

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
                                "container": {"padding": "5!important", "background-color": "#29355c"},
                                "icon": {"color": "orange", "font-size": "30px"}, 
                                "nav-link": {"font-size": "12px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#02ab21"},
                                }, orientation='vertical')






#### Function for displaying map ####
def display_map(location, parameter):
    #### Create folium map markers: ####
    au = folium.Marker(
                location=[56.166666 , 10.1999992],
                popup=f"Aarhus University  -{parameter}",
                icon=folium.Icon(color="blue", icon="home"),
                )

    ruc = folium.Marker(
                location=[55.652330724, 12.137999448],
                popup=f"Roskilde University  -{parameter}",
                icon=folium.Icon(color="black", icon="home"),
                )

    ku = folium.Marker(
            location=[55.674497302, 12.570164386],
            prefix='fa',
            popup=f'Københavns Universitet  -{parameter}',
            icon=folium.Icon(icon='home', color='red'),
            
            )
    
    map = folium.Map(location=(56.263920, 10.501785),
                    zoom_start=7,
                    scrollWheelZoom=True,
                    tiles='cartodbpositron'
                    
                    
                    
                    )
    if location == 'All':
        ku.add_to(map)
        ruc.add_to(map)
        au.add_to(map)

    if location == 'Københavns University':

        ku.add_to(map)
        
    if location == "Roskilde University":

        ruc.add_to(map)

    if location == "Aarhus University":

        au.add_to(map)


    st_map = st_folium(map, width=1000, height=600)



#### Creating the dashboard section ####
def dashboard():
        ## Section description ##
        st.title("Danmarks Frie Forskningsfond")
        st.write("Visualization of funding data & funding flows")
        
    
        st.markdown("***")

        ## Adding page break ##
        for i in range(2):
            st.write('\n')


        ## Create columns for page split ##
        maincol, mapcol = st.columns([1,3])
        

        ## Choosing a visualization ##
        with maincol:
        
            chart_select = st.selectbox("Select a graph/chart", ("Map", "Heatmap", "Sankey Chart", "Histogram"))
            st.markdown("***")
            

        ## Displaying map and data on map
        with mapcol:
            
            ## Add configuration to map ##
            if chart_select == "Map":

                with maincol:
                    
                    locations = st.selectbox("Choose location to mark", ("All","Københavns University", "Roskilde University", "Aarhus University"))

                    par_select = st.selectbox("Select a parameter for funding", ("Danish Crowns (DKK)", "Percentage (%)"))

                    
            
                
                display_map(locations, par_select)

            
        
            st.slider("Year", min_value=min(years), max_value=max(years))
        


#### Creating the About section ####
def about():
    st.title("About the Visualizer")
    st.write("How do i use the visualizer and what can it tell me?")

    st.markdown("***")

    st.title("About the Data")
    st.write("How do i use the visualizer and what can it tell me?")

    ## Add creator as expander with info with git links ##
    with st.sidebar:
        
        with st.expander("Creators"):
            textcol, linkcol = st.columns(2)

            with textcol:

                st.write("Andreas LN")
                st.markdown("***")
                st.write("Christoffer M.K.")
                st.markdown("***")
                st.write("Gustav C.")
                st.markdown("***")
            
            with linkcol:
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
                st.write(aln_git)
                for i in range(5):
                    st.write('\n')
                st.write(cmk_git)
                for i in range(5):
                    st.write('\n')
                st.write(gc_git)
               


#### Checking for user choice and displaying context of menu ####
if choose == "Dashboard":
    dashboard()
    

if choose == "About":
    about()


    
    


    
        

    
    









