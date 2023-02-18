""" 
I separated the assignments into functions. They are called at the bottom of this file.
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
    but I think it's nice to also be able to see many of them at once.
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
        user_input = str(input('     Input:'))

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
            # fb_sorted.iloc[row_index]['density']:.1f extracts population density with one decima
            main_title = f"The population density of {user_input} is {fb_sorted.iloc[row_index]['density']:.1f} people per km^2"
            assignment_2_plot(df_country, main_title)

        else:
            print('The input was incorrect, please provide a new input')
            print('')
            print('')
            is_input_bad = True # We were proven otherwise, go back in the loop



####################################### 3 start #######################################

def assignment_3_choice_1(_df_cia_factbook):
    """ Solution for choice 1 """
    # The test creates a bool-mask based on the assignment criteria
    test =  \
            (_df_cia_factbook['population'] > _df_cia_factbook['population'].mean()) & \
            (_df_cia_factbook['area'] < _df_cia_factbook['area'].mean()) & \
            (_df_cia_factbook['birth_rate'] >= 15) & \
            (_df_cia_factbook['birth_rate'] <= 24) & \
            (_df_cia_factbook['life_exp_at_birth'] > 70)

    df_filtered = _df_cia_factbook[test] # df_filtered is a dataframe with the filtered countries

    # This step is unnecessary because no country that fulfill the criteria contain NaN
    # I don't think they can have any NaN but I include the line anyway because of the instructions
    df_result = df_filtered.dropna(subset=['population', 'area', 'life_exp_at_birth', 'birth_rate'])

    # I tried to match the example output
    print('     Geographically small, high population countries with high birth ')
    print('     rate and high life expectancy:')
    print('')
    print('     Country:              Area:              Number of Births:        Life Expectancy:')
    print('                           [km^2]             [per 1000 inhabitants]')
    print('-----------------------------------------------------------------------------------------')

    # Loop over all filtered rows (countries)
    for _, row in df_result.iterrows():
        # I set a desired length of the strings and add padding (spaces)
        padding_country = max(22 - len(row['country']), 0)
        padding_area = max(22 - len(str(row['area'])), 0)
        print(\
                " "*5 +\
                row['country'] + " "*padding_country +\
                str(row['area']) + " "*padding_area +\
                str(row['birth_rate']) + " "*20 +\
                str(row['life_exp_at_birth']))
    print('')


def assignment_3_choice_2(_df_cia_factbook):
    """ Solution for choice 2 """
    # I decided to create the extra column in multiple steps to make it easier to read
    internet_quotient = _df_cia_factbook['internet_users'] / _df_cia_factbook['population']
    internet_density = internet_quotient * 100000
    _df_cia_factbook['internet_density'] = internet_density

    # Remove all NaN in the dataset
    df_cleaned = _df_cia_factbook.dropna(subset=['internet_density'])
    # Sort the dataset from lowest to highest internet density
    df_sorted = df_cleaned.sort_values(by='internet_density')

    # Create a dataframe containing the 5 lowest internet density countries
    df_lowest = df_sorted[:5]

    # The dataframe containing the 5 highest internet density countries is resorted from high to low
    df_highest = df_sorted[-5:]
    df_highest = df_highest.sort_values(by='internet_density', ascending=False)

    # I tried to match the example output but needed more space (literary)
    # This because Congo has such a ridiculously long name...
    print('')
    print(' The countries with lowest and highest quotient of internet users:')
    print('     Country:                           Population:           Internet users:          ')
    print('                                                              [per 100000 inhabitants] ')
    print('---------------------------------------------------------------------------------------')

    # Country name, population and internet user per 100000 people are printed
    # Same as choice 1, I add padding to get all rows lined up
    print('Lowest:')
    for _,row in df_lowest.iterrows():
        padding_country = max(35 - len(row['country']), 0)
        padding_population = max(22 - len(str(row['population'])), 0)
        print(\
                " "*5 +\
                row['country'] + " "*padding_country +\
                f"{int(row['population'])}" + " "*padding_population +\
                f"{row['internet_density']:.2f}") # This could probably be done prettier...
    print('Highest:')
    for _,row in df_highest.iterrows():
        padding_country = max(35 - len(row['country']), 0)
        padding_population = max(22 - len(str(row['population'])), 0)
        print(\
                " "*5 +\
                row['country'] + " "*padding_country +\
                f"{int(row['population'])}" + " "*padding_population +\
                f"{row['internet_density']:.2f}")
    print('')


def assignment_3_choice_3(_df_cia_factbook):
    """ Solution for choice 3 """
    # Calculate the population growth rate in percent
    population_growth_rate = (  + _df_cia_factbook['birth_rate']\
                                - _df_cia_factbook['death_rate']\
                                + _df_cia_factbook['net_migration_rate'])\
                                * 0.1 # This is times 100 for percent divided på 1000 

    _df_cia_factbook['population_growth_rate'] = population_growth_rate

    df_cleaned = _df_cia_factbook.dropna(subset=['population_growth_rate'])
    df_sorted = df_cleaned.sort_values('population_growth_rate')

    df_lowest = df_sorted[:5]

    df_highest = df_sorted[-5:]
    df_highest = df_highest.sort_values('population_growth_rate', ascending=False)

    # I needed extra padding here as well because of a little weird silly country
    # called "Saint Pierre and Miquelon"
    print('')
    print(' The Countries with highest percentage population decline and growth: ')
    print('   Country:                   Births rate:    Death rate:     Net migration:  Population change')
    print('                             [/1000 people]  [/1000 people]   [/1000 people]   [percent]')
    print('---------------------------------------------------------------------------------------------------')

    # Country name, population and internet user per 100000 people are printed
    # Same as choice 1, I add padding to get all rows lined up
    print('Highest decline:')
    for _,row in df_lowest.iterrows():
        string_country = row['country']
        string_birth = f"{row['birth_rate']:.1f}"
        string_death = f"{row['death_rate']:.1f}"
        string_migration = f"{row['net_migration_rate']:.1f}"
        string_growth = f"{row['population_growth_rate']:.1f}"

        padding_country = max(30 - len(string_country), 0)
        padding_birth = max(16 - len(string_birth), 0)
        padding_death = max(16 - len(string_death), 0)
        padding_migration = max(16 - len(string_migration), 0)

        print(\
                " "*3 +\
                string_country + " "*padding_country +\
                string_birth + " "*padding_birth +\
                string_death + " "*padding_death +\
                string_migration + " "*padding_migration +\
                string_growth)

    print('Highest growth:')
    for _,row in df_highest.iterrows():
        string_country = row['country']
        string_birth = f"{row['birth_rate']:.1f}"
        string_death = f"{row['death_rate']:.1f}"
        string_migration = f"{row['net_migration_rate']:.1f}"
        string_growth = f"{row['population_growth_rate']:.1f}"

        padding_country = max(30 - len(string_country), 0)
        padding_birth = max(16 - len(string_birth), 0)
        padding_death = max(16 - len(string_death), 0)
        padding_migration = max(16 - len(string_migration), 0)

        print(\
                " "*3 +\
                string_country + " "*padding_country +\
                string_birth + " "*padding_birth +\
                string_death + " "*padding_death +\
                string_migration + " "*padding_migration +\
                string_growth)
    print('')


def assignment_3_print_menu():
    """ Print out the menu text"""
    print('')
    print('############################## Assignment 2 ##############################')
    print('')
    print('     Press 1 to view geographically small, high population countries with high birth ')
    print('     rate and high life expectancy')
    print('     Press 2 to view the countries with lowest and highest internet user')
    print('     density')
    print('     Press 3 to view the countries with highest and lowest population')
    print('     growth (or decline) per 1000 inhabitants')
    print('')
    print('     Press 4 to exit program')
    print('     press 0 to view menu again')
    print('')


def assignment_3(_df_cia_factbook):
    """ My solution to assignment 3 """
    # Call the print menu function
    assignment_3_print_menu()

    # is_running controls the while loop
    is_running = True
    while is_running:
        # User menu input is stored in "choice"
        # choice = input('     Choose a menu option (0 for info): ')
        choice = '3'
        print('')
        print('')

        # Call the functions based on the user input
        if choice == '1':
            assignment_3_choice_1(_df_cia_factbook)
            input('press enter')
        elif choice == '2':
            assignment_3_choice_2(_df_cia_factbook)
            input('press enter')
        elif choice == '3':
            assignment_3_choice_3(_df_cia_factbook)
            # input('press enter')
        # choice 4 stops the program
        elif choice == '4':
            print('Program stop')
            is_running = False
        # 0 reprints the menu options
        elif choice == '0':
            assignment_3_print_menu()
        # A simple else to handle incorrect user input
        else:
            print('     Incorrect input, please try again')

        # Add extra rows to separate outputs
        print('')
        print('')

        is_running = False



##################### This is where the assignments are called ########################

# The data in the csv-files are stored in dataframe objects with correct names
# This needs to be done to enable the other assignments
df_cia_factbook, df_worldcities, df_worldpubind = assignment_1() # assignment_1 returns the data


# assignment_2(df_cia_factbook)
assignment_3(df_cia_factbook)
