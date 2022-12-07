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


## Load dataset
df = pd.read_csv('gustav/dff.csv', index_col=False)



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


## Filter function / Display filters ##
@st.experimental_memo
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







## Generate sankey chart ##
@st.experimental_memo
def generateSankey(df, year, category_columns):
    df.tail()

    colorpalette = px.colors.qualitative.Plotly

    # data for sankey
    df = df.loc[df['År'] == year]
    df_sankey = df.loc[:,category_columns + ['Bevilliget beløb']]

    # create list of labels, i.e. unique values from each column except the values
    # create color list
    labels = []
    colornumlist = []

    for col in category_columns:
        labels = labels + list(set(df_sankey[col].values)) # adds unique labels in each category to list
        colornumlist.append(len(list(set(df_sankey[col].values)))) # appends number of unique labels for each category

    # define colors based on number of categories
    colorList = []
    for idx, colorNum in enumerate(colornumlist):
        colorList = colorList + [colorpalette[idx]]*colorNum

    # initiate input for for loop
    df_link_input = pd.DataFrame({'source' : [], 'target': [], 'count': []})

    # create data for go.Sankey function
    for i in range(len(category_columns)-1):
        if len(category_columns) == 1:
            print("Number of input categories must be at least 2")
        else:
            temporary_df = df_sankey.groupby([category_columns[i], category_columns[i+1]]).agg({'Bevilliget beløb':'sum'}).reset_index() # loop over columns and group by column to the right, i.e. 'År' and 'Virkemidler', and then 'Virkemidler' and 'Område'
            temporary_df.columns = ['source','target','count']
            df_link_input = df_link_input.append(temporary_df)

    # add index for source-target pair
    df_link_input['sourceID'] = df_link_input['source'].apply(lambda x: labels.index(x))
    df_link_input['targetID'] = df_link_input['target'].apply(lambda x: labels.index(x))

    # creating the sankey diagram
    fig = go.Figure(data=[go.Sankey(
        valueformat = ",",
        valuesuffix = " kr.",
        # define nodes
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = colorList
            ),
        link = dict(
            source = df_link_input['sourceID'], # indices correspond to labels, e.g. '2022', 'Forskningsprojekt 1', 'Forskningsprojekt 2', ...
            target = df_link_input['targetID'],
            value = df_link_input['count']
        ))])

    fig.update_layout(title_text="Funding of Research Grants in " + str(year) + "<br>Source: <a href='https://dff.dk/'>Danmarks Frie Forskningsfond</a>",
                        font_size=10)
    return fig


## Generate wordcloud ##

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

    



#### Creating the dashboard section ####
st.cache()
def dashboard():
    with st.sidebar:
        with st.container():
            with st.expander("Filters", expanded=True):

                locations = st.selectbox("Choose an institution", institution)

                #theme = st.selectbox("Choose a theme", omraade)

                #year = st.selectbox("Year", years)

                #charts = st.multiselect("Choose visualizers", ['Funding flow', 'Top funded words', 'Funding wordcloud'], default="Funding flow")
                
                dashtype = st.radio("Choose dashboard type", ['Investigator', 'Comparer'])
                
        
        with st.container():
            with st.expander('Need instructions?'):
                st.write("How to use:")

        
    
    
    if dashtype == 'Comparer':
        maincol1, maincol2, maincol3 = st.columns([3,1,1])        
        

        with maincol2:
            compare = st.selectbox(f"Compare {locations} with:", options=institution)

        with maincol3:
            charts = st.multiselect("Chosen visualizers", ['Funding flow', 'Top funded words', 'Funding wordcloud'], default="Funding flow")
        
        with maincol1:

            st.metric(f"Institution(s)", value=f'{locations} and {compare}', )
        "---"

        sandcol1, sandcol2 = st.columns([2,2])
        with sandcol1:

            if 'Funding flow' in charts:
                with st.expander(f"Funding flow for {locations}", expanded=True):
                    for pagebreak in range(2):
                        "\n"

                    CHOICES = {1: "Virkemidler", 2: "Område"}

                    def format_func(option):
                        return CHOICES[option]

                    
                    option1 = st.selectbox("Column 2. Data", options=[CHOICES.get(1), CHOICES.get(2)], index=0)
                    option2 = st.selectbox("Column 3. Data", options=[CHOICES.get(1), CHOICES.get(2)], index=1)
                    year_slider = st.slider("Year", min_value=2013, max_value=2022, value=2013)
                        
                    
                    with st.container():
                        
                        # NODES UDE TIL HØJRE SKAL SORTERES I FALDENDE ORDEN
                        # plotting sankey diagram
                        if locations == 'All':
                            
                            if option1 == 'Virkemidler' and option2 == 'Område':
                                sankey = generateSankey(df, year=year_slider, category_columns = ['År',option1, option2])
                                st.plotly_chart(sankey, use_container_width=True)

                            elif option1 == 'Område' and option2 == 'Virkemidler':
                                sankey = generateSankey(df, year=year_slider, category_columns = ['År',option1, option2])
                        
                        
                                st.plotly_chart(sankey, use_container_width=True)
                            
                        else:

                            if option1 == 'Virkemidler' and option2 == 'Område':
                                sankey = generateSankey(df.loc[(df["Institution"] == locations)], year=year_slider, category_columns = ['År',option1, option2])
                                st.plotly_chart(sankey, use_container_width=True)

                            elif option1 == 'Område' and option2 == 'Virkemidler':
                                sankey = generateSankey(df.loc[(df["Institution"] == locations)], year=year_slider, category_columns = ['År',option1, option2])
                                st.plotly_chart(sankey, use_container_width=True)

        

                with sandcol2:
                    with st.expander(f"Funding flow for {compare}", expanded=True):
                        for pagebreak in range(2):
                            "\n"

                        CHOICES = {1: "Virkemidler", 2: "Område"}

                        def format_func(option):
                            return CHOICES[option]

                        
                        option3 = st.selectbox(f"Column 2. Data ", options=[CHOICES.get(1), CHOICES.get(2)], index=0)
                        option4 = st.selectbox(f"Column 3. Data ", options=[CHOICES.get(1), CHOICES.get(2)], index=1)
                        year_slider = st.slider(f"Year ", min_value=2013, max_value=2022, value=2013)
                            
                        
                        
                        
                        with st.container():
                            
                            # NODES UDE TIL HØJRE SKAL SORTERES I FALDENDE ORDEN
                            # plotting sankey diagram
                            if compare == 'All':
                                
                                if option3 == 'Virkemidler' and option4 == 'Område':
                                    sankey = generateSankey(df, year=year_slider, category_columns = ['År',option3, option4])
                                    st.plotly_chart(sankey, use_container_width=True)

                                elif option3 == 'Område' and option4 == 'Virkemidler':
                                    sankey = generateSankey(df, year=year_slider, category_columns = ['År',option3, option4])
                            
                            
                                    st.plotly_chart(sankey, use_container_width=True)
                                
                            else:

                                if option3 == 'Virkemidler' and option4 == 'Område':
                                    sankey = generateSankey(df.loc[(df["Institution"] == compare)], year=year_slider, category_columns = ['År',option1, option2])
                                    st.plotly_chart(sankey, use_container_width=True)

                                elif option3 == 'Område' and option4 == 'Virkemidler':
                                    sankey = generateSankey(df.loc[(df["Institution"] == compare)], year=year_slider, category_columns = ['År',option1, option2])
                                    st.plotly_chart(sankey, use_container_width=True)
            
            if locations or compare == 'All':
                with sandcol1:
                    if 'Top funded words' in charts:
                        with st.expander(f"Top funded words ({locations})", expanded=True):
                            with st.container():
                                ## Display bar chart ##
                                total_bar_chart = generate_bar_chart(df, animated=True)
                                st.plotly_chart(total_bar_chart, use_container_width=True)
                    with sandcol2:
                        with st.expander(f"Top funded words ({compare})", expanded=True):
                            with st.container():
                                ## Display bar chart ##
                                total_bar_chart = generate_bar_chart(df, animated=True)
                                st.plotly_chart(total_bar_chart, use_container_width=True)
            
            else:
                with sandcol1:
                    if 'Top funded words' in charts:
                        with st.expander(f"Top funded words ({locations})", expanded=True):
                            with st.container():
                                ## Display bar chart ##
                                total_bar_chart = generate_bar_chart(df.loc[(df["Institution"] == locations)], animated=True)
                                st.plotly_chart(total_bar_chart, use_container_width=True)
                    
                    with sandcol2:
                        with st.expander(f"Top funded words ({compare})", expanded=True):
                            with st.container():
                                ## Display bar chart ##
                                total_bar_chart = generate_bar_chart(df.loc[(df["Institution"] == compare)], animated=True)
                                st.plotly_chart(total_bar_chart, use_container_width=True)


                    
                
        with sandcol1:
            if 'Funding wordcloud' in charts:
                with st.expander("Funding wordcloud", expanded=True):
                    cloudcol1, cloudcol2, cloudcol3 = st.columns([5,2,5])
                    with cloudcol2:
                        with st.container():
                            ## Display Wordcloud ##
                            
                            fig2 = gen_wordcloud()
                            fig2 = st.image(fig2.to_array())
                            

        for break_page in range(2):
            st.write("\n")

    #### INVESTIGATOR SECTION ####
    if dashtype == 'Investigator':
        maincol1, maincol2, maincol3 = st.columns([4,2,4])  
        with maincol1:
            st.write("Institution")
            st.subheader(f"{locations}")
            for i in range(2):
                "\n"
            
        
        with maincol2:
            if locations == 'All':
                all_sum = sum(df["Bevilliget beløb"])
                st.write("Total funding 2013-2022")
                st.subheader(f'{all_sum:,} DKK')

            else:
                metricdata = df.loc[df["Institution"] == locations]
                metricsum = metricdata["Bevilliget beløb"]

                st.write("Total funding 2013-2022")
                st.subheader(f"{sum(metricsum):,} DKK")
                for i in range(5):
                    "\n"
        
        sub_chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="sankey", title="🔴Funding flow", description=""),
        stx.TabBarItemData(id="barchart", title="🟢Most used words", description=""),
        stx.TabBarItemData(id="bubblechart", title="🟡Most funded words (Bubblechart)", description=""),
        stx.TabBarItemData(id="wordcloud", title="🟣Most funded words (Wordcloud)", description="")
        ])
        investicol1,investicol2,investicol3 = st.columns([0.5,20,0.5])

        if sub_chosen_id == 'barchart':
            with investicol2:

                with st.container():
                    ## Display bar chart ##
                    total_bar_chart = generate_bar_chart(df.loc[(df["Institution"] == locations)], animated=True)
                    st.plotly_chart(total_bar_chart, use_container_width=True)
        
        elif sub_chosen_id == 'bubblechart':
            with investicol2:

                with st.container():
                    animated_bub = generate_bubble_chart(df, animated = True)
                    st.plotly_chart(animated_bub)
                
        

        if 'sankey' in sub_chosen_id:
            for pagebreak in range(2):
                "\n"
            CHOICES = {1: "Virkemidler", 2: "Område"}


            def format_func(option):
                return CHOICES[option]
            
            flowfilter1, flowfilter2, flowfilter3 = st.columns([1,1,1])
            
            with flowfilter1:    
                option1 = st.selectbox("Column 2. Data", options=[CHOICES.get(1), CHOICES.get(2)], index=0)
            with flowfilter2:  
                option2 = st.selectbox("Column 3. Data", options=[CHOICES.get(1), CHOICES.get(2)], index=1)
            with flowfilter3:  
                option2 = st.selectbox("Column X. Data", options=[CHOICES.get(1), CHOICES.get(2)], index=1)
            
            year_slider = st.slider("Year", min_value=2013, max_value=2022, value=2013)
            
            
            
            
            with st.container():
                
                # NODES UDE TIL HØJRE SKAL SORTERES I FALDENDE ORDEN
                # plotting sankey diagram
                if locations == 'All':
                    
                    if option1 == 'Virkemidler' and option2 == 'Område':
                        sankey = generateSankey(df, year=year_slider, category_columns = ['År',option1, option2])
                        st.plotly_chart(sankey, use_container_width=True)

                    elif option1 == 'Område' and option2 == 'Virkemidler':
                        sankey = generateSankey(df, year=year_slider, category_columns = ['År',option1, option2])
                
                
                        st.plotly_chart(sankey, use_container_width=True)
                    
                    
                else:

                    if option1 == 'Virkemidler' and option2 == 'Område':
                        sankey = generateSankey(df.loc[(df["Institution"] == locations)], year=year_slider, category_columns = ['År',option1, option2])
                        st.plotly_chart(sankey, use_container_width=True)

                    elif option1 == 'Område' and option2 == 'Virkemidler':
                        sankey = generateSankey(df.loc[(df["Institution"] == locations)], year=year_slider, category_columns = ['År',option1, option2])
                        st.plotly_chart(sankey, use_container_width=True)
                        
                        
                        
                        

            for break_page in range(2):
                st.write("\n")

        
        #WORD CLOUD #
        elif sub_chosen_id == 'wordcloud':
            cloudcol1, cloudcol2, cloudcol3 = st.columns([1,2,1])
            with st.expander("Funding wordcloud", expanded=True):
                

                with cloudcol2:
                    with st.container():
                        ## Display Wordcloud ##
                        wordcloud_freqs = generate_wordcloud_freqs(df)
                        wordcloud = generate_wordcloud_funding(df.loc[(df["Institution"] == locations)])
                        st.image(wordcloud.to_array(), width=700)

            for break_page in range(2):
                st.write("\n")


        # datacol1,datacol2,datacol3 = st.columns([1,10,1])

        # with datacol2:
        #     with st.container():
    #             dataset = filters(locations, 'All', 2022)
    #             st.dataframe(dataset)
            

    
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




#### Checking for user navigation choice and displaying context of menu ####
if choose == "Dashboard":
    dashboard()
    

if choose == "About":
    about()


    