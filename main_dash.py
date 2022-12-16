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
			@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Poppins';

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
                                "container": {"padding": "5!important", "background-color": "#ffffff"},
                                "icon": {"color": "orange", "font-size": "15px"}, 
                                "nav-link": {"font-size": "13px", "text-align": "left", "margin":"5px", "--hover-color": "#306fff"},
                                "nav-link-selected": {"background-color": "#306fff"},
                                }, orientation='horizontal')
    
    
    with st.sidebar:
        
        with st.expander("Filters", expanded=True):

            dashtype = st.radio("Select dashboard view", ['Investigate', 'Compare'])
            if dashtype == 'Investigate':

                locations = st.selectbox("Select institution", institution)

                #theme = st.selectbox("Choose a theme", omraade)

                #year = st.selectbox("Year", years)

                #charts = st.multiselect("Choose visualizers", ['Funding flow', 'Top funded words', 'Funding wordcloud'], default="Funding flow")
                
                

                if locations == "All":
                    df = full_df
                else:
                    df = full_df.loc[(full_df["Institution"] == locations)]

                df2 = full_df
            
            if dashtype == 'Compare':
                locations = st.selectbox("Select institution", institution)
                comp_loc = st.selectbox("Select institution to compare", institution)

                #theme = st.selectbox("Choose a theme", omraade)

                #year = st.selectbox("Year", years)

                #charts = st.multiselect("Choose visualizers", ['Funding flow', 'Top funded words', 'Funding wordcloud'], default="Funding flow")
                
                

                if locations == "All":
                    df = full_df
                else:
                    df = full_df.loc[(full_df["Institution"] == locations)]

                if comp_loc == "All":
                    df2 = full_df
                else:
                    df2 = full_df.loc[(full_df["Institution"] == comp_loc)]

            

        
        with st.expander('Need instructions?'):

            st.write(
                """
                You can choose either *Invesitigate* or *Compare* view.
                Investigate lets you see a detailed visualization of funding, word usage and other statistics for an insitution. \n
                Compare lets you compare general statistics between each chosen instituions.
                When using compare view, you need to select multiple institutions from the selectboxes above.
                """)
#### Creating the dashboard section ####
st.cache()
def dashboard(df, df2):
    
    #### Investigate SECTION ####

    if dashtype == 'Investigate':
        maincol1, maincol2 = st.columns([2,2], gap="large")  
        with maincol1:
            st.title("Funding overview")
            st.write("Institution")
            st.subheader(f"{locations}")
            
        
        with maincol2:
            for line_break in range(6):
                "\n"
            year = st.select_slider("Use the slider below to select a year",
                                    options=[2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,"All Time"],
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
        
        tab1, tab2 = st.tabs(["Funding flow", "Funding timeline"])

        with tab1:
            st.text("")
            st.text("")
            st.write(
            """
            This Sankey chart displays how the funding is flowing from a given year to a funding mechanism, and to a scientific area.
            By hovering over each bar, you can get more detailed information about the funding flow and the exact amount of funding.   
            """)  
            sankey = generateSankey(df, year=year, category_columns=['År','Virkemidler', 'Område'])
            st.plotly_chart(sankey, use_container_width=True)     
        "---"
        if not len(df) == 0: 
            st.cache()
            avg_funding, funding, freqs =  generate_data(df = df,
                                                        funding_thresh_hold = 0)
            st.cache()
            all_words = get_all_words(df)
            st.title(f"Word Explorer")
            st.write(
                """
                The word explorer lets you explore how often words are used, how titles, containing certain words are funded, and how often certain words appears together titles.
                You can chose *All Words*, which gives a general overview of the most used words, words that appears most often together, and highest funded words.
                Or you can choose *Specific Words*, which lets you choose specific words to explore and compare their funding, usage in titles, and their appearences with other words.
                """)

            all_specific = st.radio("**Click on an option below to explore either all words or specific words**", options=['All Words', 'Specific Words'] )
            if all_specific == 'Specific Words':
                selected_words = st.multiselect("Select Word:", options = all_words, default = all_words[0], ) 
            "---"
            if all_specific == 'Specific Words':
                word_col1, word_col2, word_col3, word_col4, word_col5, word_col6 = st.columns([1,3,3,3,3,1], gap="medium")  
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
                # Extra linespace
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                with st.expander("*Description*"):
                    st.write(
                        """
                        - *Combined Funding:* Sum of all funding for titles which contain the chosen word.
                        - *Average Funding:* The average funding for each title containing the chosen word, calculated thusly: *Combined Funding / Times Used in Title*
                        - *Times Used in Title:* How many different titles The word appears in.
                        """)                
                "---"
                with st.expander(("**Explore How Often Selected Words Co-Appears in Titles**"), expanded=False):
                    st.write(
                    """
                    The Connectivity Graphs takes your previously selected words and generates a network graph.
                    The graph displays how frequently these words appear together in titles.
                    The more often two words appear together in titles, the larger the line between them will be. 
                    Therefore, words, which often appear togther in will have a more visible line between them.
                    You can hover over the small number between the lines to see how strong the connection between two words are.
                    You can likewise hover over a word marker, to learn more about the word's funding, total connectivity and total appearances in titles (frequency).
                    Moreover, the size of the word marker is determined by its general connectivity.
                    The general connectivity is a number for how many unique words a given word appears together with across all titles.\n
                    If a word is not displayed, it means that it does not appear in the same title as any of the selected words.
                    If no words are displayed, none of the selected words appear together in a title. 
                    """)
                    activate_btn = st.button("*Click here to display Connectivty Graph*", key="activate1")
                    if activate_btn:
                        graph_chart = generate_graph_words(df, words= selected_words)
                        st.plotly_chart(graph_chart, use_container_width=True)
                    
                with st.expander("**Explore Which Words Most Often Appear in the Same Title as a Chosen Word**", expanded=False):      
                    st.write(
                    """
                    This Connectivity Graphs takes a single selected word and generates a network graph.
                    The graph displays which words (stopwords excluded) most frequently appear together with your chosen word.
                    The more often a word appear together with your chosen word, the larger the line between them will be. 
                    Therefore, words, which often appear in the same title as the chosen word, will have a more visible line between them.
                    You can hover over the small number between the lines to see how strong the connection between two words are.
                    You can likewise hover over a word marker, to learn more about the word's funding, total connectivity and total appearances in titles (frequency).
                    Moreover, the size of the word marker is determined by its general connectivity.
                    The general connectivity is a number for how many unique words a given word appears together with across all titles.\n
                    You can select which word to explore in the box below this text.
                    """)

                    select_word = st.selectbox("*Click Here To Choose Word :*", options = selected_words, label_visibility = "hidden")

                    st.write("Use the slider below to choose how many word connections (number of lines) you wish to display.")
                    
                    top_n_investigation = st.select_slider("Top word connections",
                                options=[i for i in range(2, 81)],
                                value = 10,
                                key = "word_investigation_slider",
                                label_visibility = "hidden")
                    if select_word is not None:
                        graph_chart_single = generate_graph_single_word(df, word=select_word, top_n = top_n_investigation)
                        st.plotly_chart(graph_chart_single, use_container_width=True)   
                
                with st.expander("**Explore Combined Funding and Average Funding for Selected Words**", expanded=False):
                    st.write(
                        """
                        This bubble plot displays the combined funding vertically and the average funding horizontally for each of the selected words.
                        Word markers at the top of the plot have a high combined funding, and word markers at the furthest right have a high average funding.
                        The color and size indicates how many titles the word appears in (word frequency).
                        You can hover over the word marker to get the exact numbers for its funding and appearences in titles.  
                        """)
                    words_bub_chart = generate_bubble_words(df, words = selected_words, animated=False)
                    st.plotly_chart(words_bub_chart, use_container_width=True)

                with st.expander("**Explore Word Frequencies for Selected Words**"):
                    st.write(
                        """
                        This barchart displays the frequencies of all the selected words.
                        The color of the bars indicates how high average funding each word has.
                        You can hover over the bars to get the exact numbers for its funding and appearences in titles (frequency).
                        """)
                    barchart_words = generate_bar_chart(df, words = selected_words)
                    st.plotly_chart(barchart_words, use_container_width=True) 

            if all_specific == 'All Words':
                with st.expander("**Explore Which Words Most Frequently Appear in the Same Title**", expanded=False):
                    st.write(
                    """
                    This network graph displays which words (stopwords excluded) most frequently appear in the same title.
                    The more often two words appear together the larger the line between them will be. 
                    Therefore, words, which often appear in the same title, will have a more visible line between them.
                    You can hover over the small number between the lines to see how strong the connection between two words are.
                    Moreover, the size of the word marker is determined by its general connectivity.
                    The general connectivity is a number for how many unique words a given word appears together with across all titles.\n
                    """)
                    
                    slider_label = "Use the slider below to choose how many word connections (number of lines) you wish to display."
                    top_n = st.select_slider(slider_label,
                                options=[i for i in range(2, 81)],
                                value = 10,
                                key = "top_n_words_slider")
                    graph_chart = generate_graph_top_n(df, top_n)
                    st.plotly_chart(graph_chart, use_container_width=True)
                
                with st.expander("**Words With Highest Combined Funding**", expanded=False):
                    st.write(
                        """
                        This bubble plot shows the words with the highest combined funding and plots it.
                        The combined funding is indicated vertically and the average funding horizontally.
                        Word markers at the top of the plot have a high combined funding, and word markers at the furthest right have a high average funding.
                        The color and size indicates how many titles the word appears in (word frequency).
                        You can hover over the word marker to get the exact numbers for its funding and appearences in titles.  
                        """)
                    top_n = st.select_slider("Use the slider below to change how many words you wish to display.",
                                options=[i for i in range(10, 81)],
                                value = 50,
                                key = "top_n_bub_slider")
                    bubchart = generate_bubble_chart(df, top_n = top_n, animated = False)
                    st.plotly_chart(bubchart, use_container_width=True)
                
                with st.expander("**Words Used in Most Titles**"):
                    st.write(
                        """
                        This barchart displays the words which appears in most titles.
                        The colors of the bars indicates how much average funding each word has.
                        You can hover over the bars to get the exact numbers for its funding and appearences in titles (frequency).
                       """)
                    top_n = st.select_slider("Use the slider below to change how many words you want to display.",
                                options=[i for i in range(10, 81)],
                                value = 50,
                                key = "top_n_bar_slider")
                    barchart = generate_bar_chart(df, animated = False, top_n = top_n)
                    st.plotly_chart(barchart, use_container_width=True)

            full_screen_fix()
    
    if dashtype == 'Compare':
        
        maincol1, maincol2 = st.columns([3,3], gap="large")  
        with maincol1:
            st.write("Institutions")
            st.subheader(f"{locations} & {comp_loc}")
        
            for linebreak in range(2):
                "\n"
        
        
        with maincol2:
            year = st.select_slider("**Use the slider below to select a year**",
                                    options=[2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,"All Time"],
                                    value='All Time')
                                          
            
        
            if year == "All Time":
                df = df
                df2 = df2
            if not year == "All Time":
                df = df.loc[(df["År"] == year)]
                df2 = df2.loc[(df2["År"] == year)]
    
        "---"
        expcol1, expcol2 = st.columns([2,2])
        
        with expcol1:
            with st.expander(f'{locations}', expanded=True):
                
                st.write("Year selected:")
                st.subheader(year)
                
                all_sum1 = sum(df["Bevilliget beløb"])
                st.write(f"Total funding:")
                
                st.subheader(f'{all_sum1:,} DKK')
            
                num_projects = len(df)
                st.write(f"Number of funded projects:")
                st.subheader(f'{num_projects}')
            
        
                avg_fund = all_sum1//num_projects
                st.write(f"Average funding pr. project:")
                st.subheader(f'{avg_fund:,} DKK')

        with expcol2:
            with st.expander(f'{comp_loc}', expanded=True):
                
                st.write("Year selected:")
                st.subheader(year)
                
                all_sum2 = sum(df2["Bevilliget beløb"])
                st.write(f"Total funding:")
                st.subheader(f'{all_sum2:,} DKK')
            
                num_projects2 = len(df2)
                st.write(f"Number of funded projects:")
                st.subheader(f'{num_projects2}')
            
        
                avg_fund2 = all_sum2//num_projects2
                st.write(f"Average funding pr. project:")
                st.subheader(f'{avg_fund2:,} DKK')
        
                


   

        








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

    st.dataframe(df)



if choose == "Dashboard":
    dashboard(df, df2)

if choose == "About":
    about()
            
    


