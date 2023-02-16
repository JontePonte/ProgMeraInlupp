"Example 1"

import pandas as pd


def assignment_1():
    """ 
    Uppgift 1 
    Load all data and clean it up, then return all three as Dataframe objects 
    """

    # I set index_col='Index' to avoid an unnecessary index row
    # The drop unnamed: 0 is done to avoid a second unnecessary index row
    _factbook = pd.read_csv('cia_factbook.csv', sep=';', index_col='Index')
    _factbook = _factbook.drop("Unnamed: 0", axis=1) 

    # I thought about using the city id as index but I didn't because
    # it's difficult to refer to. (=a vanilla read_csv here)
    _cities = pd.read_csv('worldcities.csv', sep=';')

    # I remove the columns "Indicator Name" and "Indicator Code" because
    # they hold no valuable data
    _pubind = pd.read_csv('worldpubind.csv', sep=';')
    _pubind = _pubind.drop(columns=["Indicator Name", "Indicator Code"])

    return _factbook, _cities, _pubind


factbook, cities, pubind = assignment_1()

print(pubind)

