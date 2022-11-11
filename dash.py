# Import modules. Check requirements.txt for dependencies
import streamlit as st
from streamlit_option_menu import option_menu
#import streamlit.components.v1 as html
#from  PIL import Image
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io
import pydeck as pdk



# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state="auto")




# Markdown code to hide "hamburger-menu"
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True,)





#with col2:
    #st.write("This i col2")

# Creating data objects
data1 = [
    [x for x in range(3)]
    ]

data2 = [
    [x for x in range(3)]
    ]

data3 = [
    [x for x in range(3)]
    ]


#### Configuring Sidebar/Navigation bar ####
with st.sidebar:
    choose = option_menu("Navigation bar", ["Dashboard", "About"],
                         icons=['speedometer', 'question-square'],
                         menu_icon="segmented-nav", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#000000"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "12px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }, orientation='vertical'
    )


cities = pd.DataFrame({
    'Location' : ['Denmark'],
    'lat' : [55.676098],
    'lon' : [12.568337]
})


#### Checking for user choice and displaying context of menu ####
if choose == "About":
    st.title("About")
    st.write("This is the About section")
    st.markdown("***")
    


if choose == "Dashboard":

    st.title("Danmarks Frie Forskningsfond")
    with st.expander("What is DFF?"):
        st.header("What is DFF?")
        st.write("DFF is a funding institution")
        
        
        

    st.markdown("***")
    
    st.header("Explore the data")


    maincol, mapcol = st.columns(2)
    with maincol:
        with st.expander("About the charts"):
            st.subheader("Explanation")
            st.write("SDU = Syddansk Universitet")


    with mapcol:
        cat_select = st.selectbox("Select a parameter for funding", ("Danish Crowns (DKK)", "Percentage (%)"))
        chart_select = st.selectbox("Select a graph/chart", ("Map", "Heatmap", "Sankey Chart", "Histogram"))
        if chart_select == "Map":
            
            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                latitude=56.263920,
                longitude=10.501785,
                zoom=6,
                pitch=None)))
                
            #st.map(data=None, zoom=10000000000000, use_container_width=False)
            val = st.slider("Choose a year", min_value=1900, max_value=2022)
        
       

        
            #st.markdown("***")
    
    
        

    
    









