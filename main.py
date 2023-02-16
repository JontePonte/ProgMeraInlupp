"I separate all assignments into functions."

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


# The dataframe objects are stored with their correct names
df_cia_factbook, df_worldcities, df_worldpubind = assignment_1()


####################################### 2 start #######################################

# Calculate the population density using area and population in cia_factbook
# All NaN and inf needs to be removed

# Take user input 7+ to display the seven highest densities, 5- to display the five lowest
# User can also input a country name and then get the population density for that country

# Display highest/lowest densities in a bar diagram
# Or 
# Display the density of the selected country (maybe plus countries higher/lower, all in bar diagram) 