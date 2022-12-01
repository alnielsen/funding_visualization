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
#from christoffer.text_viz import generate_data, gen_bubble_data, create_bar_plot, create_bubble_plot, create_wordcloud

# Set page configuration
st.set_page_config(page_title="Funding Visualization Project", page_icon=":moneybag:", layout="wide", initial_sidebar_state="expanded")


## Load dataset
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


## Generate bar plots ##
@st.experimental_memo
def gen_bar_plots():

    avg_funding, funding, freqs = generate_data(df = df,
                                            funding_thresh_hold = 0)
#############
# Bar plots #
#############
    TOP_N = 30



    fig_funding = create_bar_plot(data_dict = funding,
                                color_dict = freqs,
                                color_label = "# of Grants Containing Word",
                                value_label = "Funding across all grants",
                                title = f"Top {TOP_N} words with highest funding ",
                                top_n = TOP_N)
    return fig_funding


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
            df_link_input = df_link_input.concat(temporary_df)

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
@st.experimental_memo
def gen_wordcloud():
    avg_funding, funding, freqs = generate_data(df = df,
                                            funding_thresh_hold = 0)
    
    wc = create_wordcloud(size_dict=funding, color_dict=freqs)

    return wc
    

## Generate and display map ##
def display_map(institution, tema):

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    location = geolocator.geocode(institution)

    lat = location.latitude
    lon = location.longitude

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    tooltip = 'Show info.'
    
    map = folium.Map(location=map_data, zoom_start=10, scrollWheelZoom=False, width='100%', height="100%")
    folium.Marker(
    [lat, lon], popup=f'{institution}', tooltip=tooltip
    ).add_to(map)
    return map


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
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="Investigate", title="🔍 Investigate", description=""),
        stx.TabBarItemData(id="Sandbox", title="📊 Sandbox", description="")], default="Investigate")
    
    with st.sidebar:
        with st.container():
            with st.expander("Filters", expanded=True):

                locations = st.selectbox("Choose an institution", institution)

                #theme = st.selectbox("Choose a theme", omraade)

                #year = st.selectbox("Year", years)

                
        
        with st.container():
            with st.expander('Need instructions?'):
                st.write("How to use:")

        
    
    
    if chosen_id == 'Sandbox':
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


            if 'Top funded words' in charts:
                with st.expander("Top funded words", expanded=True):
                    
                    with st.container():
                        ## Display bar plots ##
                        fig1 = gen_bar_plots()
                        st.plotly_chart(fig1, use_container_width=True)

                
                
        with sandcol1:
            if 'Funding wordcloud' in charts:
                with st.expander("Funding wordcloud", expanded=True):
                    cloudcol1, cloudcol2, cloudcol3 = st.columns([5,2,5])
                    with cloudcol2:
                        with st.container():
                            ## Display Wordcloud ##
                            
                            fig2 = gen_wordcloud()
                            st.image(fig2.to_array())

        for break_page in range(2):
            st.write("\n")

    if chosen_id == "Investigate":
        metriccol, spacecol, viscol = st.columns([3,1,1])
        with metriccol:

            st.metric("Institution: ", value=locations)
            
        with viscol:
            charts = st.multiselect("Choose visualizers", ['Funding flow', 'Top funded words', 'Funding wordcloud'], default="Funding flow")
        if 'Funding flow' in charts:
            with st.expander(label="Funding flow",expanded=True):
                for pagebreak in range(2):
                    "\n"
                CHOICES = {1: "Virkemidler", 2: "Område"}


                def format_func(option):
                    return CHOICES[option]

                flowfilter1, flowfilter2 = st.columns([1,1])
                year_slider = st.slider("Year", min_value=2013, max_value=2022, value=2013)
                with flowfilter1:    
                    option1 = st.selectbox("Column 2. Data", options=[CHOICES.get(1), CHOICES.get(2)], index=0)
                with flowfilter2:  
                    option2 = st.selectbox("Column 3. Data", options=[CHOICES.get(1), CHOICES.get(2)], index=1)
                
                
                dashcol1,dashcol2,dashcol3 = st.columns([1,10,1])
                with dashcol2:
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

        if 'Top funded words' in charts:
            with st.expander("Top funded words", expanded=True):
                barcol1, barcol2, barcol3 = st.columns([1,10,1])

                with barcol2:
                    with st.container():
                        ## Display bar plots ##
                    
                        fig1 = gen_bar_plots()
                        st.plotly_chart(fig1, use_container_width=True)

            
            for break_page in range(2):
                st.write("\n")

        if 'Funding wordcloud' in charts:
            with st.expander("Funding wordcloud", expanded=True):
                cloudcol1, cloudcol2, cloudcol3 = st.columns([5,2,5])

                with cloudcol2:
                    with st.container():
                        ## Display Wordcloud ##
                        
                        fig2 = gen_wordcloud()
                        st.image(fig2.to_array())

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


    