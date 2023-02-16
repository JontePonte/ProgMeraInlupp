"Example 1"

import pandas as pd

####################################### 1 start #######################################
def assignment_1():
    """ 
    Uppgift 1 
    Load all data and clean it up, then return all three as Dataframe objects 
    """

    # I set index_col='Index' to avoid an unnecessary index row
    # The drop unnamed: 0 is done to avoid a second unnecessary index row
    fact_book = pd.read_csv('cia_factbook.csv', sep=';', index_col='Index')
    fact_book = fact_book.drop("Unnamed: 0", axis=1) 

    # I thought about using the city id as index but I didn't because
    # it's difficult to refer to. (=a vanilla read_csv here)
    world_cities = pd.read_csv('worldcities.csv', sep=';')

    # I remove the columns "Indicator Name" and "Indicator Code" because
    # they hold no valuable data
    world_pub_ind = pd.read_csv('worldpubind.csv', sep=';')
    world_pub_ind = world_pub_ind.drop(columns=["Indicator Name", "Indicator Code"])

    return fact_book, world_cities, world_pub_ind


df_cia_factbook, df_worldcities, df_worldpubind = assignment_1()

##################################### 1 finished #####################################

print(df_worldpubind)

