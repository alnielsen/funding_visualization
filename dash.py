# Import modules. Check requirements.txt for dependencies
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io


# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state='expanded')

# Markdown code to hide "hamburger-menu"
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


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
    }, orientation='horizontal'
    )


#### Checking for user choice and displaying context of menu ####
if choose == "About":
    st.title("About")
    st.write("This is the About section")
    st.markdown("***")
    


if choose == "Dashboard":
    st.title("Dashboard")
    st.write("This is the dashboard")
    st.markdown("***")
    
    
    sel_box = st.selectbox("Available data", ["--Pick an option--","Data1", "Data2", "Data3"], args=None)

    

    if sel_box == "Data1":
        st.write("**Data1**")
        st.table(data1)
    
    if sel_box == "Data2":
        st.write("**Data2**")
        st.table(data2)
    
    if sel_box == "Data3":
        st.write("**Data3**")
        st.table(data3)









