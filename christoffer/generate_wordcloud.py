import pandas as pd
from utils import create_wordcloud
from math import inf

def filter_dict(dictionary, lower_thresh = 0, upper_thresh = inf):
    filtered_dict = {}
    for key, val in dictionary.items(): 
        if  lower_thresh <= val <= upper_thresh:
            filtered_dict[key] = val
    return filtered_dict


def create_color_dict(size_dict, non_filtered_dict):
    """
    Creates a color dict, which contains the same keys as the size dict
    """
    filtered_color_dict = {}
    for key in size_dict:
        val = non_filtered_dict[key]
        filtered_color_dict[key] = val
    return filtered_color_dict

def dict_is_empty(dictionary):
    return not bool(dictionary)    


def generate_data(year: int = None, # For filtering
                       min_abs_amount = 0, # For filtering
                       min_rel_amount = 0, # Filtering
                       min_freq = 0, # Filtering
                       min_rel_freq = 0, # Filtering
                       show: bool = False,
                       save_path: str = None):

    df = pd.read_csv("../synthetic_data.csv")
    if year is not None:
        df = df[df["år"] == year]
    df["title_desc"] = df["titel"] + df["beskrivelse"]

    n_words = 0
    funding_sum = sum(df["beløb"])

    abs_freqs = {} # Absolute frequencies
    rel_freqs = {} # Relative frequencies
    abs_funding = {} # Absolute funding recieved
    rel_funding = {}# Relative funding recieved

    # Create dict of absolute freqs and funding
    for text, amount in zip(df["title_desc"], df["beløb"]):
        # Split each token/word on whitespace
        tokens = set([token.lower() for token in text.split()]) # Get unique tokens

        n_words += len(tokens)
        for token in text.split():
            token = token.lower()
            if not token in abs_freqs:
                abs_freqs[token] = 1
                abs_funding[token] = amount
            else:
                abs_freqs[token] += 1
                abs_funding[token] += amount

    # Create dict for relative freqs
    for key, val in abs_freqs.items():
        rel_freqs[key] = val/n_words

    # I think there is a mistake here - FIXME
    # Create dict for relative funding
    for key, val in abs_funding.items():
        rel_funding[key] = val/funding_sum
    
    return (abs_funding, rel_funding, abs_freqs, rel_freqs)


#Demonstrating filtering and creation
for year in range(2013, 2022 + 1):
    abs_funding, rel_funding, abs_freqs, rel_freqs = generate_data(year)
    
    # Size = abs funding, color = abs freqs
    size_dict = filter_dict(abs_funding, 1000) # At least 1000 kr. in funding
    if dict_is_empty(size_dict):
        size_dict = abs_funding # no filter if empty
    
    color_dict = create_color_dict(size_dict, abs_freqs)
    f_path = f"output/abs funding/abs_funding_{year}.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                               color_dict = color_dict,
                               title = f"Absolute funding and word usage {year}",
                               show = False,
                               save_path = f_path)

    # size = rel funding, color = rel freq
    size_dict = filter_dict(rel_funding, 0.05) # 5% of funding
    
    if dict_is_empty(size_dict):
        size_dict = rel_funding # no filter if empty
    
    color_dict = create_color_dict(size_dict, rel_freqs)
    f_path = f"output/relative_funding/rel_funding_{year}.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                               color_dict = color_dict,
                               title = f"Relative funding and word usage {year}",
                               show = False,
                               save_path = f_path)

    # size = abs freq, color = abs funding
    size_dict = filter_dict(abs_freqs, 2) # lowest frequency is 2
    
    if dict_is_empty(size_dict):
        size_dict = abs_freqs # no filter if empty
    
    color_dict = create_color_dict(size_dict, abs_funding)
    f_path = f"output/abs_freqs/abs_freq{year}.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                               color_dict = color_dict,
                               title = f"Absolute word frequency and funding {year}",
                               show = False,
                               save_path = f_path)
                               
    # size = rel freq, color = rel funding
    size_dict = filter_dict(rel_freqs, 2) # lowest frequency is 2
    
    if dict_is_empty(size_dict):
        size_dict = rel_freqs # no filter if empty
    
    color_dict = create_color_dict(size_dict, rel_funding)
    f_path = f"output/rel_freqs/rel_freq{year}.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                               color_dict = color_dict,
                               title = f"Relative word frequency and funding {year}",
                               show = False,
                               save_path = f_path)

'''
# Test
abs_funding, rel_funding, abs_freqs, rel_freqs = generate_data()


size_dict = create_color_dict(filter_dict(abs_funding, 0, 15000), abs_freqs)# betweem 0 and 15.000 kr. in funding
if not dict_is_empty(size_dict):
    f_path = f"output/size_test/abs_funding_betwen_0_15000.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                                title = f"Absolute funding and word usage between 0 and 15000",
                                show = True,
                                height = 200,
                                save_path = f_path)

size_dict = create_color_dict(filter_dict(abs_funding, 15000, 25000), abs_freqs)# between 15 and 25.000 kr. in funding
if not dict_is_empty(size_dict):
    f_path = f"output/size_test/abs_funding_between_15000_25000.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                                title = f"Absolute funding and word usage between 15000 and 25000",
                                show = True,
                                height = 300,
                                save_path = f_path)

size_dict = create_color_dict(filter_dict(abs_funding, 25000, 50000), abs_freqs)# between 25 and 50.000 kr. in funding
if not dict_is_empty(size_dict):
    f_path = f"output/size_test/abs_funding_between_25000_50000.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                                title = f"Absolute funding and word usage between 25000 and 50000",
                                show = True,
                                height = 400,
                                save_path = f_path)

                    
size_dict = create_color_dict(filter_dict(abs_funding, 50000, 75000), abs_freqs)# between 50 and 75.000 kr. in funding
if not dict_is_empty(size_dict):
    f_path = f"output/size_test/abs_funding_betweem_50000_75000.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                                title =f"Absolute funding and word usage between 50000 and 75000",
                                show = True,
                                height = 500,
                                save_path = f_path)

size_dict = create_color_dict(filter_dict(abs_funding, 75000), abs_freqs)# above 75.000 kr. in funding
if not dict_is_empty(size_dict):
    f_path = f"output/size_test/abs_funding_above_75000.jpg"
    w_cloud = create_wordcloud(size_dict = size_dict,
                                title = f"Absolute funding and word usage above 75000",
                                show = True,
                                height = 600,
                                save_path = f_path)
'''