# Import modules. Check requirements.txt for dependencies
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
from streamlit_folium import st_folium
import folium
import random as rd
import csv
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from generate_wordcloud import generate_data, create_wordcloud


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



#### Function for displaying map ####
def display_map(location):#, parameter):
    #### Create folium map markers: ####
    au = folium.Marker(
                location=[56.166666 , 10.1999992],
                popup=f"Aarhus University",
                icon=folium.Icon(color="blue", icon="home"),
                )

    ruc = folium.Marker(
                location=[55.652330724, 12.137999448],
                popup=f"Roskilde University",
                icon=folium.Icon(color="black", icon="home"),
                )

    ku = folium.Marker(
            location=[55.674497302, 12.570164386],
            prefix='fa',
            popup=f'Copenhagen Universitet',
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



#### Histogram function ####
def histo_chart():

                arr = [x for x in range(500)]
                fig1, ax1 = plt.subplots()
                ax1.hist(arr, bins=20)
                st.plotly_chart(fig1)



#### Bankey chart function ####
def bankey_chart():
    fig3 = go.Figure(data=[go.Sankey(
                    node = dict(
                    pad = 15,
                    thickness = 20,
                    line = dict(color = "white", width = 0),
                    label = ["A1", "A2", "B1", "B2", "C1", "C2"],
                    color = "blue"
                    ),
                    link = dict(
                    source = [0, 1, 0, 2, 3, 3], # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target = [2, 3, 3, 4, 4, 5],
                    value = [8, 4, 2, 8, 4, 2]
                ))])

    fig3.update_layout(title_text="Basic Sankey Diagram", font_size=20)

    st.plotly_chart(fig3)




#### Creating the dashboard section ####
def dashboard():


        
        title_col1, title_col2 = st.columns([2,3])
        with title_col1:
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

                
            
        
        ## Create upper filter columns
        dashcol2, dashcol3 = st.columns([2,2], gap="large")

        

        ## MAP CHART ##
        with dashcol2:
            with st.container():
                with st.expander("Open/Collapse Map", expanded=False):

                    display_map(locations)

            ## HISTORGRAM ##
                with st.container():
                    with st.expander("Open/Collapse Histogram", expanded=False):
                        histo_chart()



        ## DATA CHART ##
        with dashcol3:
            with st.container():
                
                with st.expander(label="Open/Collapse Wordcloud", expanded=False):
                    dataframe = df
                    
                    if locations == 'All' and theme == 'All' and year == 'All':
                        
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(df)
        
                        

                    elif locations == 'All' and theme == theme and year == 'All':

                        dataframe = df.loc[(df['Område'] == theme)]
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(dataframe)

                    elif locations == locations and theme == 'All' and year == 'All':
                        
                        dataframe = df.loc[(df['Institution'] == locations)]
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(dataframe)

                    
                    elif year == year and locations == 'All' and theme == 'All':
                        dataframe = df.loc[(df['År'] == year)]
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(dataframe)
                    

                    elif locations == 'All' and theme == theme and year == year:
                        dataframe = df.loc[(df['Område'] == theme) & (df['År'] == year)]
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(dataframe)


                    elif locations == locations and theme == 'All' and year == year:
                        dataframe = df.loc[(df['Institution'] == locations) & (df['År'] == year)]
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(dataframe)
                    
                    elif locations == locations and theme == theme and year == 'All':
                        dataframe = df.loc[(df['Institution'] == locations) & (df['Område'] == theme)]
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(dataframe)
                         
                    
                    else:
                        locations = locations
                        theme = theme
                        year = year
                        dataframe = df.loc[(df['Institution'] == locations) & (df['Område'] == theme) & (df['År'] == year)]
                        # funding_thresh = st.slider("Funding amount", min_value=min(dataframe['Bevilliget beløb']), max_value=max(dataframe['Bevilliget beløb']))
                        # funding, freqs = generate_data(dataframe, funding_thresh)
                        # w_cloud = create_wordcloud(size_dict=funding, color_dict=freqs)
                        # st.image(w_cloud.to_array())
                        with title_col2:
                            for i in range(12):
                                "\n"
                            st.dataframe(dataframe)
                    
                    
                    
                    source = 'Soruce: [Danmarks Frie Forskningsfond](https://dff.dk/forskningsprojekter)'
                    st.markdown(source, unsafe_allow_html=True)
                #par_select = st.selectbox("Select a parameter for funding", ("Danish Crowns (DKK)", "Percentage (%)"))
                ## SANKEY CHART ##
        
                with st.container():
                    with st.expander("Open/Collapse Sankey Chart", expanded=False):
                        bankey_chart()
        

        
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
    


    
        

    
    









