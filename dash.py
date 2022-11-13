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
import random as rd
import csv


# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state="auto")



years = [x for x in range(1900,2023)]

df = pd.read_csv('gustav/dff.csv')


institution = []

for i in df['Institution']:
    if i not in institution:
        institution.append(i)


omraade = []

for i in df['Område']:
     if i not in omraade:
        omraade.append(i)




#nums_dat.drop(nums_dat.filter(regex="Unname"),axis=1, inplace=True)




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
                                "container": {"padding": "5!important", "background-color": "#181a30"},
                                "icon": {"color": "orange", "font-size": "20px"}, 
                                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#02ab21"},
                                }, orientation='horizontal')






#### Function for displaying map ####
def display_map(location, parameter):
    #### Create folium map markers: ####
    au = folium.Marker(
                location=[56.166666 , 10.1999992],
                popup=f"Aarhus University",
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
            popup=f'Copenhagen Universitet  -{parameter}',
            icon=folium.Icon(icon='home', color='red'),
            
            )
    
    map = folium.Map(location=(56.253920, 15.501785),
                    zoom_start=6,
                    scrollWheelZoom=True,
                    tiles='cartodbpositron'
                    
                    
                    
                    )
    if location == 'All':
        ku.add_to(map)
        ruc.add_to(map)
        au.add_to(map)

    if location == 'Københavns Universitet':

        ku.add_to(map)
        
    if location == "Roskilde Universitet":

        ruc.add_to(map)

    if location == "Aarhus Universitet":

        au.add_to(map)


    st_map = st_folium(map, width=900, height=450)



#### Creating the dashboard section ####
def dashboard():
        ## Section description ##
        st.title("Danmarks Frie Forskningsfond")
        st.subheader("Visualization of funding data & funding flows")

       
        dashcol1, dashcol2 = st.columns([1,4])
        with dashcol1:

            chart_select = st.selectbox("Select a graph/chart", ("Overview", "Map", "Heatmap", "Sankey Chart", "Histogram"))
    
        st.markdown("***")

        

        ## Choosing a visualization ##
        
        ## Add configuration to map ##
        if chart_select == "Overview":
             ## Create columns for page split ##
            maincol, datacol = st.columns([2,5])

            with maincol:



                locations = st.selectbox("Choose an institution", (institution))

                theme = st.selectbox("Choose a theme", (omraade))

                #par_select = st.selectbox("Select a parameter for funding", ("Danish Crowns (DKK)", "Percentage (%)"))


            with datacol:

                st.dataframe(df.loc[(df['Institution'] == locations)])
                source = 'Soruce: [Danmarks Frie Forskningsfond](https://dff.dk/forskningsprojekter)'
                st.markdown(source, unsafe_allow_html=True)


                
        

        if chart_select == "Map":
            ## Create columns for page split ##
            maincol, mapcol = st.columns([2,3])
        


            with maincol:

                locations = st.selectbox("Choose an institution", (institution))

                par_select = st.selectbox("Select a parameter for funding", ("Danish Crowns (DKK)", "Percentage (%)"))

            with mapcol:
                display_map(locations, par_select)

            #st.select_slider("Year", years)    

        
        
                
        


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
    


    
        

    
    









