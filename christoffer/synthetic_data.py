import pandas as pd
from random_word import Wordnik
from random import randint

df = pd.DataFrame(columns = [
    
    "titel",
    "beskrivelse",
    "modtager",
    "institution",
    "område",
    "virkemiddel",
    "beløb",
    "år"
])



def _generate_random_paragrah(low_len, high_len):
    """
    Generates a full random paragrah between low_len and high_len length 
    """
    word_lim = randint(low_len, high_len)
    if word_lim == 0:
        return ""
    else:      
        random_words = Wordnik().get_random_words(limit = word_lim) 
        paragraph = ""
        try:
            for word in random_words:
                paragraph += f"{word} "
        except TypeError:
            paragraph = "ERROR"
        return paragraph



institutioner = ["AU", "SDU", "AAU", "KU", "ITU", "ROC"]
områder = [f"område {i}" for i in range(8)]
virkemidler = [f"virke {i}" for i in range(10)]
for _ in range(4000):
    # All values are in list for eaiser conversion to pandas
    row = {
        "titel": [_generate_random_paragrah(5, 15)],
        "beskrivelse": [_generate_random_paragrah(0, 250)],
        "modtager": [_generate_random_paragrah(1,  4)],
        "institution": [institutioner[randint(0, len(institutioner) - 1)]],
        "område": [områder[randint(0, len(områder) - 1)]],  
        "virkemiddel": [virkemidler[randint(0, len(virkemidler) - 1)]],
        "beløb": [randint(10000, 5000000)],
        "år": [randint(2013, 2022)]       
    }
    print(_)
    df = pd.concat([df, pd.DataFrame.from_dict(row)], ignore_index=True)
df.to_csv("../synthetic_data.csv")