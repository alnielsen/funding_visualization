
import streamlit as st 
import streamlit_wordcloud as wordcloud
import pandas as pd

def generate_data_dicts(year: int = None):

    df = pd.read_csv("../synthetic_data.csv")
    if year is not None:
        df = df[df["år"] == year]
    df["title_desc"] = df["titel"] + df["beskrivelse"]

    words = []
    n_words = 0
    funding_sum = sum(df["beløb"])

    abs_freqs = {} # Absolute frequencies
    rel_freqs = {} # Relative frequencies
    abs_funding = {} # Absolute funding recieved
    rel_funding = {}# Relative funding recieved

    # Create dict of absolute freqs and funding
    for text, amount in zip(df["title_desc"], df["beløb"]):
        # Split each token/word on whitespace
        tokens = text.split()
        n_words += len(tokens)
        for token in text.split():
            word_dict = {}
            token = token.lower()
            if not token in abs_freqs:
                abs_freqs[token] = 1
                rel_freqs[token] = 1/n_words
                abs_funding[token] = amount
            else:
                abs_freqs[token] += 1
                rel_freqs[token] += 1/n_words
                abs_funding[token] += amount
                rel_funding[token] += amount / funding_sum
    
    for key in abs_funding:
        word_dict = dict(text = key,
                         value = abs_funding[key],
                         relative_funding = rel_funding[key],
                         frequency = abs_freqs[key],
                         relative_frequency = rel_freqs[key])
        words.append(word_dict)
    return word_dict

    
    data_dicts = [abs_funding, rel_funding,]

st.set_page_config(layout="centered")

st.title("Streamlit WordCloud Component")
st.write("This is an example of how you might use the Streamlit wordcloud component and retrieve its response object.")
'''
# Using Wordcloud component
words = [
    dict(text="Robinhood", value=16000, color="#b5de2b", country="US", industry="Cryptocurrency"),
    dict(text="Personio", value=8500, color="#b5de2b", country="DE", industry="Human Resources"),
    dict(text="Boohoo", value=6700, color="#b5de2b", country="UK", industry="Beauty"),
    dict(text="Deliveroo", value=13400, color="#b5de2b", country="UK", industry="Delivery"),
    dict(text="SumUp", value=8300, color="#b5de2b", country="UK", industry="Credit Cards"),
    dict(text="CureVac", value=12400, color="#b5de2b", country="DE", industry="BioPharma"),
    dict(text="Deezer", value=10300, color="#b5de2b", country="FR", industry="Music Streaming"),
    dict(text="Eurazeo", value=31, color="#b5de2b", country="FR", industry="Asset Management"),
    dict(text="Drift", value=6000, color="#b5de2b", country="US", industry="Marketing Automation"),
    dict(text="Twitch", value=4500, color="#b5de2b", country="US", industry="Social Media"),
    dict(text="Plaid", value=5600, color="#b5de2b", country="US", industry="FinTech"),
]
return_obj = wordcloud.visualize(words, tooltip_data_fields={
    'text':'Company', 'value':'Mentions', 'country':'Country of Origin', 'industry':'Industry'
}, per_word_coloring=False)

# Output the response Object
st.header("1. Response object:\n")
st.write(return_obj)

# Usage example code
st.header("2. Usage Example")
st.markdown("""
```python
import streamlit as st 
import streamlit_wordcloud as wordcloud

words = [
    dict(text="Robinhood", value=16000, color="#b5de2b", country="US", industry="Cryptocurrency"),
    dict(text="Personio", value=8500, color="#b5de2b", country="DE", industry="Human Resources"),
    dict(text="Boohoo", value=6700, color="#b5de2b", country="UK", industry="Beauty"),
    dict(text="Deliveroo", value=13400, color="#b5de2b", country="UK", industry="Delivery"),
    dict(text="SumUp", value=8300, color="#b5de2b", country="UK", industry="Credit Cards"),
    dict(text="CureVac", value=12400, color="#b5de2b", country="DE", industry="BioPharma"),
    dict(text="Deezer", value=10300, color="#b5de2b", country="FR", industry="Music Streaming"),
    dict(text="Eurazeo", value=31, color="#b5de2b", country="FR", industry="Asset Management"),
    dict(text="Drift", value=6000, color="#b5de2b", country="US", industry="Marketing Automation"),
    dict(text="Twitch", value=4500, color="#b5de2b", country="US", industry="Social Media"),
    dict(text="Plaid", value=5600, color="#b5de2b", country="US", industry="FinTech"),
]
return_obj = wordcloud.visualize(words, tooltip_data_fields={
    'text':'Company', 'value':'Mentions', 'country':'Country of Origin', 'industry':'Industry'
}, per_word_coloring=False)
```
""")
# Available Options
st.header("3. .visualize() Method Options")
st.markdown("""
| Prop  | Default | Type | Description |
| :------------ | :---------------:| :---------------:| ---------------|
| words | `None` | `list[dict]` | List of word dictionaries to be used for wordcloud visualiztion. Required keys: `'text', 'value'`. Optional keys: `'color'`, `<-Any Additional Meta Key->` |
| width | `'100%'` | `str` | Width of wordcloud |
| height | `None` | `str` | Height of wordcloud |
| font_min | `None` | `int` | Smallest font size of words in wordcloud |
| font_max | `None` | `int` | Largest font size of words in wordcloud |
| font_scale | `None` | `float` | The scaling factor which will be multiplied by the default font sizes. `font_scale` can only effects if no `font_min` or `font_max` has been passed. |
| max_words | `None` | `int` | Maximum number of words to be displayed on wordcloud. |
| palette | `viridis` | `str` | Color palette to be used for the words in the wordcloud. This will only have an effect if `per_word_coloring` is set to `False`. Available Options: [`Matplotlib Colormaps`](https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html) |
| per_word_coloring | `False` | `bool` | If `True`, the `color` key in the `words` objects will be used to fill the words in wordcloud. |
| padding | `1` | `int` | Padding between words in word cloud. |
| layout | `'rectangular'` | `str` | Wordcloud layout. Available options: `['rectangular', 'archimedean']` |
| enable_tooltip | `True` | `bool` | Whether to show tooltip popover once hover on a word. |
| tooltip_data_fields | `{'text':'Word', 'value':'Count'}` | `dict` | A dictionary containing keys and their displayed values to be used in tooltip. The keys in this dictionary can only be selected from the ones passed in the `words` dictionaries. |
| key | `None` | `str` | An optional key that uniquely identifies this Streamlit component. |
""")

'''