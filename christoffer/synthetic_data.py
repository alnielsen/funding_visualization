import pandas as pd
from random_word import Wordnik
from random import randint


df = {
    "titel": [],
    "beskrivelse": [],
    "modtager": [],
    "institution": [],
    "område": [],
    "virkemiddel": [],
    "beløb": [],
    "år": []    
}



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
for _ in range(3700):
    # All values are in list for eaiser conversion to pandas
    
    df["titel"].append(_generate_random_paragrah(5, 15))
    df["beskrivelse"].append(_generate_random_paragrah(5, 15))
    df["modtager"].append(_generate_random_paragrah(1,  4))
    df["institution"].append(institutioner[randint(0, len(institutioner) - 1)])
    df["område"].append(områder[randint(0, len(områder) - 1)])
    df["virkemiddel"].append(virkemidler[randint(0, len(virkemidler) - 1)])
    df["beløb"].append(randint(10000, 5000000))
    df["år"].append(randint(2013, 2022))

    print(_)
df = pd.DataFrame.from_dict(df)
df.to_csv("../synthetic_data.csv")