"Example 1"

import pandas as pd

factbook = pd.read_csv('cia_factbook.csv', sep=';', index_col='Index')
factbook = factbook.drop("Unnamed: 0", axis=1) 
# I set index_col='Index' and drop the unnamed because the dataset contain 3 index columns otherwise

cities = pd.read_csv('worldcities.csv', sep=';')
pubind = pd.read_csv('worldpubind.csv', sep=';')

print(factbook)
