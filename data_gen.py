import pandas as pd
import numpy as np
import random
import csv
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()



uni_dat = ["Copenhagen University", "Aarhus University"]
uni = [(random.choice(uni_dat)) for y in range(300)]
nums = [(random.randint(0, 999999)) for x in range(300)]



d = {'amount': nums }



df = pd.DataFrame(d, index=uni)



f = open('syn_num.csv', 'w')

df.to_csv(f)

f.close()


print(df)