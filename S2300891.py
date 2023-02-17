""" 
I separate all assignments into functions. They can be called at the bottom of this file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

def assignment_2_plot(df_output, main_title):
    """ The plot function for assignment 2 """
    # Plot the country and density as a bar diagram without legend
    df_output.plot(x='country', y='density', kind='bar', legend=False)

    # Set all labels and print the diagram
    plt.xlabel('Country')
    plt.ylabel('[People/km^2]')
    plt.title(main_title)
    plt.show()


def assignment_2(_df_cia_factbook):
    """ 
    My solution to assignment 2. The function is called at the bottom of this file.
    I allowed more than 10 countries to be plotted. I can change it if you like
    but I think it's interesting to see many of them at once.
    """

    # Create the pandas series density and add it to df_cia_factbook dataframe
    density = _df_cia_factbook['population'] / _df_cia_factbook['area']
    _df_cia_factbook['density'] = density

    # I save the original index before dropna and sorting for a fancy plot later on
    original_index = _df_cia_factbook.index
    
    # This changes the inf for Vatican City to NaN. This enables dropna for Vatican City and
    # all other countries with NaN density
    _df_cia_factbook = _df_cia_factbook.replace({np.inf:np.nan})
    _df_cia_factbook = _df_cia_factbook.dropna(subset=['density'])

    # Sort the dataframe and put the highest density first
    fb_sorted = _df_cia_factbook.sort_values(by='density', ascending=False)
    
    # Add a sorted index to enable fancy plot later on
    fb_sorted = fb_sorted.set_index(original_index[0:fb_sorted.shape[0]])

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

    # Just a small check to enable user to fix the input
    is_input_bad = True
    while is_input_bad:
        is_input_bad = False                    # input is not bad until proven otherwise
        user_input = str(input('Input:'))

        # sort the user input based on what type it is
        if user_input[-1] == '+':               # Last character is "+"
            stop_index = int(user_input[:-1])   # Extract all numbers before "+"
            df_high = fb_sorted[0:stop_index]   # Create a dataframe from the index
            
            # Create a title for the plot and send to plot function
            main_title = f"The {stop_index} countries with highest population density"
            assignment_2_plot(df_high, main_title)

        # Basically the same as before
        elif user_input[-1] == '-':
            start_index = int(user_input[:-1])
            df_low = fb_sorted[-start_index:]

            main_title = f"The {start_index} countries with lowest population density"
            assignment_2_plot(df_low, main_title)

        # Check if user input match any of the countries
        # (I think this breaks down if the user input is for example 'a')
        elif fb_sorted['country'].str.contains(user_input).any():
            # I do a fancy thing here, 
            # I collect the 6 closest countries i a dataframe instead of just printing it
            row_index = fb_sorted.loc[fb_sorted['country'] == user_input].index[0]

            row_index = 4 if row_index < 4 else row_index
            row_index = fb_sorted.shape[0]-3 if row_index > fb_sorted.shape[0]-3 else row_index

            df_country = fb_sorted.iloc[row_index-4 : row_index+3]

            # Send the fancy dataframe and title to plotting function
            main_title = f"The population density of {user_input} and the 6 closest countries"
            assignment_2_plot(df_country, main_title)

        else:
            print('The input was incorrect, please provide a new input')
            print('')
            print('')
            is_input_bad = True # We were proven otherwise, go back in the loop



####################################### 3 start #######################################


##################### This is where the assignments are called ########################

assignment_2(df_cia_factbook)
