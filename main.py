""" 
I separate all assignments into functions.
"""

import pandas as pd
import numpy as np

####################################### 1 start #######################################
def assignment_1():
    """ Load all data and clean it up, then return all three as Dataframe objects """

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

def assignment_2(df_cia_factbook):
    """ My solution to assignment 2. The function is called just below """

    # Create the pandas series density and add it to df_cia_factbook dataframe
    density = df_cia_factbook['population'] / df_cia_factbook['area']
    df_cia_factbook['density'] = density

    # This changes the inf for Vatican City to NaN. This enables dropna for Vatican City and
    # all other countries with NaN density
    df_cia_factbook = df_cia_factbook.replace({np.inf:np.nan})
    df_cia_factbook = df_cia_factbook.dropna(subset=['density'])

    # Sort the dataframe and put the highest density first
    fb_sorted = df_cia_factbook.sort_values(by='density', ascending=False)

    print('')
    print('############################## Assignment 2 ##############################')
    print('')
    print('     List the countries with highest and lowest population density ')
    print('')
    print('     Input "7+" to display the 7 countries with highest densities')
    print('     Input "5-" to display the 5 countries with lowest densities')
    print('')
    print('     You can also input a countries name to view its density')
    print('')

    # user_input = str(input('Input:'))
    user_input = "6-"

    if user_input[-1] == '+':
        stop_index = int(user_input[:-1])
        df_high = fb_sorted[0:stop_index]
        
        print(df_high)

    elif user_input[-1] == '-':
        start_index = int(user_input[:-1])
        df_low = fb_sorted[-start_index:]

        print(df_low)

    elif fb_sorted['country'].str.contains(user_input).any():
        print(user_input + 'C!!!')
    else:
        print('no...')

    # print(fb_sorted)



assignment_2(df_cia_factbook)
