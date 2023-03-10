""" 
I separated all the assignments into functions. They are called at the bottom of this file.
This allows for the assignments to be called separately by having just one of the 
function calls uncommented at ones.

So go to the bottom of the file and try them out!
(all function calls has the corresponding line number besides them)

Assignment 1 is always called as it's needed for the other ones.

P.S.
I try to do all my programming in english. In part because I really need to practice my 
english writing but also because I downloaded a english spellchecker to vscode :)
"""
import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


####################################### 1 start #######################################

def assignment_1():
    """ Load all data and clean it up, then return all three as Dataframe objects """

    # I set index_col='Index' to avoid one unnecessary index row
    # The drop unnamed: 0 is done to avoid a second unnecessary index row
    fact_book = pd.read_csv('cia_factbook.csv', sep=';', index_col='Index')
    fact_book = fact_book.drop("Unnamed: 0", axis=1) 

    # I thought about using the city id as index but I didn't because
    # it's difficult to refer to. (= a vanilla read_csv here)
    world_cities = pd.read_csv('worldcities.csv', sep=';')

    # I remove the columns "Indicator Name" and "Indicator Code" because
    # they hold no valuable data
    world_pub_ind = pd.read_csv('worldpubind.csv', sep=';')
    world_pub_ind = world_pub_ind.drop(columns=["Indicator Name", "Indicator Code"])

    # The correct names are set at the bottom of this file
    return fact_book, world_cities, world_pub_ind


####################################### 2 start #######################################
# Assignment 2 is separated into a main function and a plot function.

def assignment_2_plot(df_output, main_title):
    """ The plot function for assignment 2 """
    # I learned to do really fancy plots in this assignment
    # First a really really fancy list comprehension that create random colors for the bars
    colors = ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(df_output.shape[0])]

    # Plot the relevant results
    axis = df_output.plot(x='country',
                        y='density',
                        kind='bar',          # Bar diagram
                        color=colors,        # Add the fancy color
                        legend=False,        # Remove unnecessary legend
                        figsize=(10,6))      # Make it bigger

    # Fix rotation and size of country names and numbers
    axis.tick_params('x', labelrotation=60, labelsize=8)
    axis.tick_params('y', labelrotation=0, labelsize=8)
    
    # Set all labels and print the diagram
    plt.xlabel('Country')
    plt.ylabel('[People/km^2]')
    plt.title(main_title)                           # Main title changes with user input
    plt.subplots_adjust(bottom=0.25)                # Put window in middle of screen
    plt.show()


def assignment_2(_df_cia_factbook):
    """ 
    My solution to assignment 2. The function is called at the bottom of this file.
    I allowed more than 10 countries to be plotted. I can change it if you like
    but I think it's interesting to also be able to see many of them at once.
    """

    # Create the pandas series "density" and add it to _df_cia_factbook dataframe
    density = _df_cia_factbook['population'] / _df_cia_factbook['area']
    _df_cia_factbook['density'] = density

    # I save the original index before dropna and sorting for a fancy extra plot later on
    original_index = _df_cia_factbook.index

    # This changes the inf for Vatican City to NaN. This enables dropna for Vatican City and
    # all other countries with NaN density (I think it's only Vatican for this data set)
    _df_cia_factbook = _df_cia_factbook.replace({np.inf:np.nan})
    _df_cia_factbook = _df_cia_factbook.dropna(subset=['density'])

    # Sort the dataframe and put the highest density first
    fb_sorted = _df_cia_factbook.sort_values(by='density', ascending=False)

    # Add a sorted index to enable the fancy plot later on
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
        is_input_bad = False # input is not bad until proven otherwise
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
        # (I think this breaks down if the user input is for example 'a' it could be done
        # better by creating a set of all countries like in later assignments)
        elif fb_sorted['country'].str.contains(user_input).any():
            # I do a fancy thing here,
            # I collect the 6 closest countries i a dataframe instead of just printing it
            row_index = fb_sorted.loc[fb_sorted['country'] == user_input].index[0]

            # The middle index is set so that the 3 highest and lowest countries can
            # be plotted (the 7 highest or lowest densities are plotted then)
            row_index = 4 if row_index < 4 else row_index
            row_index = fb_sorted.shape[0]-3 if row_index > fb_sorted.shape[0]-3 else row_index

            # Create a dataframe with the selected country and the 6 closest
            df_country = fb_sorted.iloc[row_index-4 : row_index+3]

            # Send the fancy dataframe and title to plotting function
            # fb_sorted.iloc[row_index]['density']:.1f extracts population density with one decimal
            main_title = f"{user_input} is the {row_index} densest populated country.\
 {fb_sorted.iloc[row_index]['density']:.1f} people per km^2"

            # Send to plot
            assignment_2_plot(df_country, main_title)

        else:
            print('The input was incorrect, please provide a new input')
            print('')
            print('')
            is_input_bad = True # We were proven otherwise, go back in the loop


####################################### 3 start #######################################
# I separated this one into 3 different functions fro each menu choice. Below them there
# is a little print function and the main menu function.

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

    # Add it to the main dataframe
    _df_cia_factbook['population_growth_rate'] = population_growth_rate

    # Remove all rows with NaN in population growth rate and sort 
    df_cleaned = _df_cia_factbook.dropna(subset=['population_growth_rate'])
    df_sorted = df_cleaned.sort_values('population_growth_rate')

    # df_lowest contains the countries with lowest pop growth
    df_lowest = df_sorted[:5]

    # df_highest contains the countries with highest pop growth (from high to low)
    df_highest = df_sorted[-5:]
    df_highest = df_highest.sort_values('population_growth_rate', ascending=False)

    # I needed extra padding here as well because of a little weird silly country
    # called "Saint Pierre and Miquelon"
    print('')
    print(' The Countries with Highest Percentage Population Decline and Growth [per 1000 inhabitants]: ')
    print('   Country:                   Births rate:    Death rate:     Net migration:  Population change')
    print('---------------------------------------------------------------------------------------------------')

    # The print is a bit messy. First strings are created (I choose one decimal place).
    # Then padding (of spaces) are calculated to get them under each other.
    # After that the strings and padding are printed
    print('Highest decline:')
    for _,row in df_lowest.iterrows():
        string_country = row['country']
        string_birth = f"{row['birth_rate']:.1f}"
        string_death = f"{row['death_rate']:.1f}"
        string_migration = f"{row['net_migration_rate']:.1f}"
        string_growth = f"{row['population_growth_rate']:.1f}"

        padding_country = max(30 - len(string_country), 0) # Saint Pierre are the limiting factor
        padding_birth = max(16 - len(string_birth), 0)     # 16 left some space between the header
        padding_death = max(16 - len(string_death), 0)
        padding_migration = max(16 - len(string_migration), 0)

        print(\
                " "*3 +\
                string_country + " "*padding_country +\
                string_birth + " "*padding_birth +\
                string_death + " "*padding_death +\
                string_migration + " "*padding_migration +\
                string_growth)

    # The first and second prints are the same. I could do it in a function but I thought
    # I had enough functions as it is...
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

    # Stack the lowest and highest dataframe on top of each other
    df_result = pd.concat([df_lowest, df_highest], axis=0)

    # Fancy list comprehension a barely understand that creates 10 random colors
    colors = ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(10)]

    # The plot of the results
    axis = df_result.plot(x='country',
                          y='population_growth_rate',
                          kind='bar',
                          color=colors,                    # Use the 10 random colors from above
                          legend=False,                    # Legend is unnecessary here
                          grid=True,                       # Add grid
                          figsize=(10,6))                  # Make it bigger
    
    # Fix rotation and size of country names and numbers
    axis.tick_params('x', labelrotation=60, labelsize=8)
    axis.tick_params('y', labelrotation=0, labelsize=8)

    # Titles and visual fixes to plot
    plt.subplots_adjust(bottom=0.25)                # Put window in middle of screen
    plt.title('Highest Population Decline and Highest Population Growth. (close window to view table)')
    plt.xlabel(' ')
    plt.ylabel('Population Growth Rate in Percent')
    plt.show()


def assignment_3_print_menu():
    """ Print out the menu text"""
    print('')
    print('############################## Assignment 2 ##############################')
    print('')
    print('     Press 1 to view geographically small, high population countries with high birth ')
    print('     rate and high life expectancy')
    print('     Press 2 to view the countries with lowest and highest internet user')
    print('     density')
    print('     Press 3 to view the countries with highest and lowest population growth')
    print('')
    print('     Press 4 to exit program')
    print('     press 0 to view menu again')
    print('')


def assignment_3(_df_cia_factbook):
    """ 
    My solution to assignment 3. This function is called at the bottom of the file.
    This function handles the menu and user input. Most of the code is is each choices
    functions.
    """
    # Call the print menu function
    assignment_3_print_menu()

    # is_running controls the while loop
    is_running = True
    while is_running:
        # User menu input is stored in "choice"
        choice = input('     Choose a menu option (0 for info): ')
        print('')
        print('')

        # Call the functions based on the user input
        if choice == '1':
            assignment_3_choice_1(_df_cia_factbook)
            input('press enter') # The input pauses until uses is ready
        elif choice == '2':
            assignment_3_choice_2(_df_cia_factbook)
            input('press enter')
        elif choice == '3':
            assignment_3_choice_3(_df_cia_factbook)
            input('press enter')
        # choice 4 stops the program by breaking the while loop
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


####################################### 4 start #######################################
# I split assignment 4 into two main function as they are quite separate. You need to
# call them separately.

def assignment_4a(_df_worldpubind):
    """ My solution to assignment 4a. This function is called at the bottom of this file """
    # Calculate growth between 1960 and 2021 according to formula in instructions
    growth = (_df_worldpubind['2021'] - _df_worldpubind['1960']) / _df_worldpubind['1960'] *100
    _df_worldpubind['growth'] = growth # Then add it to dataframe

    # Same old cleaning and sorting of the dataframe
    df_cleaned = _df_worldpubind.dropna(subset=['growth'])
    df_sorted = df_cleaned.sort_values('growth')

    # Same old picking out five lowest and highest
    df_lowest = df_sorted[:5]
    df_highest = df_sorted[-5:]
    df_highest = df_highest.sort_values('growth', ascending=False)

    # Create a subplot object to enable subplots ("_"=fig and isn't used)
    _, axes = plt.subplots(nrows=2,
                           ncols=1,
                           figsize=(8, 7),)

    # Same old fancy color trick as before
    colors_l = ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(5)]
    colors_h = ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(5)]

    # Plot the results
    df_lowest.plot(ax=axes[0],          # Put lowest df on top
                   x='Country Name',    # Nothing we haven't seen before
                   y='growth',
                   kind='bar',
                   color=colors_l,
                   grid=True,
                   legend=False)

    df_highest.plot(ax=axes[1],         # Put highest under
                    x='Country Name',
                    y='growth',
                    kind='bar',
                    color=colors_h,
                    grid=True,
                    legend=False)

    # Make all the labels prettier
    axes[0].tick_params('x', labelrotation=60, labelsize=8)
    axes[0].tick_params('y', labelrotation=0, labelsize=8)
    axes[1].tick_params('x', labelrotation=60, labelsize=8)
    axes[1].tick_params('y', labelrotation=0, labelsize=8)

    axes[0].set_ylabel('[Percent]', fontsize=8)
    axes[1].set_ylabel('[Percent]', fontsize=8)

    # Remove x-labels (could probably be done better)
    axes[0].set_xlabel('')
    axes[1].set_xlabel('')

    # Set titles with font size
    axes[0].set_title('Countries with highest population decline between 1960 and 2021', fontsize=10)
    axes[1].set_title('Countries with highest population growth between 1960 and 2021', fontsize=10)

    # This one sets the plots higher up on screen and add space between them
    plt.subplots_adjust(top=0.9, bottom=0.25, hspace=0.5)
    plt.show()


def assignment_4b(_df_worldpubind):
    """ My solution to assignment 4b. This function is called at the bottom of this file """

    # Print a simple menu to take the user input.
    print('')
    print('############################## Assignment 4b #############################')
    print('')
    print('        Write the name of a country to view the population change')
    print('        between 1961 and 2021.')
    print('')

    country_choice = input('        Choose a country: ')

    # Create a set of all countries in the data file to enable input check
    countries_set = set(_df_worldpubind['Country Name'].to_list())

    # Check if the user input is in the set of countries and redo the input 
    # until it is
    while not country_choice in countries_set:
        print('        The country is not in this data set. Try again')
        country_choice = input('        Choose a new country:')

    # Single out the selected country. I use a dataframe with just the
    # selected country information
    test = _df_worldpubind['Country Name'] == country_choice
    df_country_choice = _df_worldpubind.loc[test]

    # Create lists of the years and the selected country population
    years = df_country_choice.columns.tolist()[2:]
    population = df_country_choice.values.tolist()[0][2:]

    # Create a new dataframe bases on the lists
    df_populations = pd.DataFrame({'population': population, 'years': years})

    # Create a list to store population growth
    # I do this before the calculation loop to avoid append (and decrease runtime)
    # Every year that doesn't have a value should be NaN so I set all to NaN from start
    growth_list = [np.nan]*df_populations.shape[0]

    # Create iterable object for the rows
    iterator = df_populations.iterrows()
    next(iterator) # Skip 1960

    # Loop over the rows, calculate and store growth for each year from 1961
    for index, row in iterator:
        pop_the_year_before = df_populations.loc[index-1]['population']
        pop_this_year = row['population']
        growth_list[index] = (pop_this_year - pop_the_year_before) / pop_the_year_before * 100

    # Add the new growth list to the country dataframe
    df_populations['growth'] = growth_list

    # Plot the data, the fig part of this is not needed (that's why the _)
    _, axis = plt.subplots(figsize=(11, 7))

    # Plot population first
    df_populations.plot(x='years',
                        y='population',
                        ax=axis,
                        color='b')
    axis.legend(loc='upper left') # Move population legend to match instruction

    # Plot growth in the same plot
    axis2 = axis.twinx()
    df_populations.plot(x='years',
                        y='growth',
                        ax=axis2,
                        color='r')
    axis2.legend(loc='upper right') # Move growth legend to match instruction

    # Set titles and all the normal stuff
    axis.set_title(f'Population and population growth for {country_choice}')
    axis.set_xlabel('Year')
    axis.set_ylabel('Population [people] (blue)')
    axis2.set_ylabel('Population growth [percent] (red)')

    plt.show()


####################################### 5 start #######################################
# Assignment 5 is quite straight forward. Just a single function with all the data
# manipulation, prints and plots

def assignment_5(_df_worldcities):
    """ My solution to assignment 5. This function is called at the bottom of this file """
    # Group cities by country
    df_groups = _df_worldcities.groupby('country')

    # Get the index of each the biggest city of each country
    index_of_biggest_cities = df_groups['population'].idxmax()

    # Create a Series-object with the number of cities in each country
    number_of_cities = df_groups.size()
    number_of_cities = number_of_cities.sort_values(ascending=False) # And sort it

    # Pick the 10 countries with the most cities (this is also a Series-object)
    most_cities = number_of_cities[:10]

    # Prepare two lists for the upcoming super-dataframe
    biggest_cities = []
    population_of_cities = []

    # Store all needed data in the two lists by using a loop
    for country, _ in most_cities.items():
        # Get the index the biggest city in the current country
        index_of_biggest_city = index_of_biggest_cities[country]

        # Extract the biggest city and its population using the index
        biggest_city = _df_worldcities.loc[index_of_biggest_city]['city_ascii']
        population_of_city = int(_df_worldcities.loc[index_of_biggest_city]['population'])

        # I allow myself to use append here. The 10 memory jumps shouldn't
        # affect memory use and runtime to much
        biggest_cities.append(biggest_city)
        population_of_cities.append(population_of_city)

    # Create the super-dataframe from most_cities Series and the city information
    # This dataframe has all we need for the print and the plots
    df_most_cities = most_cities.to_frame()
    df_most_cities['biggest_city'] = biggest_cities
    df_most_cities['population_of_city'] = population_of_cities

    # This could be dome much better. I couldn't figure out how to rename the
    # first column in any other way...
    df_most_cities.columns = ['number_of_cities', 'biggest_city', 'population_of_city']

    print('')
    print(' The 10 countries with the highest number of cities: ')
    print('')
    print('  Country:                 Number of cities:   Biggest city:     Number of people in biggest city:')
    print('---------------------------------------------------------------------------------------------------')

    # Iterate over the super-dataframe and extract the relevant data
    for country, row in df_most_cities.iterrows(): # "country" is the super-dataframe index
        # The other info is extracted from the super-dataframe columns
        cities_in_country = row['number_of_cities']
        biggest_city = row['biggest_city']
        population_of_city = row['population_of_city']

        # Create padding to get the prints straight, the numbers match the bigger print above
        padding_country = max(25 - len(country), 0)
        padding_cities_in = max(20 - len(str(cities_in_country)), 0)
        padding_biggest_city = max(18 - len(biggest_city), 0)

        # Print everything with the right padding
        print(  "  " +\
                country + " "*padding_country +\
                str(cities_in_country) + " "*padding_cities_in+\
                biggest_city + " "*padding_biggest_city+\
                str(population_of_city))

    # Create a subplot object to enable subplots (_ = fig and isn't used)
    _, axes = plt.subplots(nrows=2,
                           ncols=1,
                           figsize=(8, 7),)
    
    # Same old fancy color trick as before
    colors = ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(10)]

    # Plot the results
    df_most_cities.plot(ax=axes[0],     # Country ad number of cities on top
                   y='number_of_cities',# I only set "y" because "x" is index=country
                   kind='bar',
                   color=colors,
                   grid=True,
                   legend=False)

    df_most_cities.plot(ax=axes[1],     # Biggest city with population below
                    x='biggest_city',
                    y='population_of_city',
                    kind='bar',
                    color=colors,       # The same (random) colors on both
                    grid=True,
                    legend=False)

    # Fix the label rotation
    axes[0].tick_params('x', labelrotation=60, labelsize=8)
    axes[0].tick_params('y', labelrotation=0, labelsize=8)
    axes[1].tick_params('x', labelrotation=60, labelsize=8)
    axes[1].tick_params('y', labelrotation=0, labelsize=8)

    # y-axis labels
    axes[0].set_ylabel('Number of Cities', fontsize=8)
    axes[1].set_ylabel('Number of People', fontsize=8)

    # Remove x-labels (could probably be done better)
    axes[0].set_xlabel('')
    axes[1].set_xlabel('')

    # Set titles with fontsize
    axes[0].set_title('The Countries with the Highest Number of Cities', fontsize=10)
    axes[1].set_title('The Biggest City in each Country', fontsize=10)

    # This one sets the plots higher up on screen and add space between them
    plt.subplots_adjust(top=0.9, bottom=0.25, hspace=0.6)
    plt.show()


##################### This is where the assignments are called ########################

# The data in the csv-files are stored in dataframe objects with correct names
# This needs to be done to enable the other assignments
df_cia_factbook, df_worldcities, df_worldpubind = assignment_1() # assignment_1 returns the data


"""
The functions for the assignments are called here. Pick one to try is out.
(you should probably only have 1 uncommented, it can get quite messy)
"""
assignment_2(df_cia_factbook)       # Starts at line 45
# assignment_3(df_cia_factbook)       # Starts at line 164
# assignment_4a(df_worldpubind)       # Starts at line 417
# assignment_4b(df_worldpubind)       # Starts at line 484
# assignment_5(df_worldcities)        # Starts at line 563
