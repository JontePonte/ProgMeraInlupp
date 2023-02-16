"Example 1"

import pandas as pd

factbook = pd.read_csv('cia_factbook.csv', sep=';')
cities = pd.read_csv('worldcities.csv', sep=';')
pubind = pd.read_csv('worldpubind.csv', sep=';')

print(pubind)
