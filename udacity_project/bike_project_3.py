import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs, change user input to lower case and add city to new york to match city_data
    while True:
        while True:
            city = input("Which cities information do you want [Chicago, Washington, New York]: ")
            if city.lower() == ("new york"):
                city = "new york city"
            if city.lower() in CITY_DATA:
                break
            else:
                print("invalid input, please enter a valid city")
        
    # TO DO: get user input for month (all, january, february, ... , june),
    # use while loop to catch invalid inputs, use months list to compare user input with
    
        months = ['all', 'january', 'february', 'march', 'april', 'may' , 'june']
        while True:
            month = input("Which month do you want data from [all , or any from January to June]: ")

            if month.lower() in months:
                break
            else:
                print("invalid input, please enter a valid month")
            
     # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
     # use while loop to catch invalid inputs, use days of week list to compare user input with.
        days_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while True:
            day = input("Which day of the week do you want data from [all, or any day monday through sunday]: ")
    
            if day.lower() in days_of_week:
                break
            else:
                print("invalid input, please enter a valid day")

        user_input = input("\nIs city:{}, month:{}, day:{} correct? Enter yes or no: ".format(city, month, day))       
        if user_input.lower() == 'yes':
            break
        else:
            print("please enter city, month, day again")

    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read csv file for user city
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    df['year_start'] = pd.DatetimeIndex(df['Start Time']).year
    
    #extract month and day of week from Start Time to create new columns
    #use to_datetime to extract month and day names from start time column
    
    df['months'] = pd.to_datetime(df['Start Time']).dt.month_name()

    df['days'] = pd.to_datetime(df['Start Time']).dt.day_name()
    
    #determine if the user input is all or is a specific month or day, then copy to dataframe
    if month.lower() != 'all':
        df_month = df[df['months'].str.contains(month.title())] 
        df = df_month.copy()
    
    if day.lower() != 'all':
        df_day = df[df['days'].str.contains(day.title())]
        df = df_day.copy()
    
    print("Looking at first rows of {}:\n {}".format(city, df.head()))
    print("\ndf shape {}".format(df.shape))
    
    while True:
        proceed = input("\nto continue enter y\n")
        if proceed == 'y':
            break
    return df
    
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    print(df.groupby('months').count())
    
    print('\nConfiguring plot for months...\n')
    month_count = df.groupby('months')['months'].count()
    
    print(month_count)
    
    see_plot = input("Would you like to see a plot of month counts? y or n ")
    if see_plot == 'y':
        month_count.plot.bar()
        plt.show()
    
       # TO DO: display the most common month
    common_month = df['months'].mode()
    print("The most popular month is {}".format(common_month))
    
    print("\nConfiguring plot for daysof the week...\n")
    
    day_count = df.groupby('days')['days'].count()
    print(day_count)
    
    see_plot = input("Would you like to see a plot of day counts? y or n ")
    if see_plot == 'y':
        day_count.plot.bar()
        plt.show()
    
    # TO DO: display the most common day of week
    common_day = df['days'].mode()
    print("The most popular day is {}".format(common_day))
    
    # TO DO: display the most common start hour
    common_hour = pd.to_datetime(df['Start Time']).dt.time.mode() 
    print("The most common hour to start is {}".format(common_hour))
    
    while True:
        proceed = input("\nto continue enter y\n")
        if proceed == 'y':
            break
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    station_counts = df.groupby('Start Station')['End Station'].count()
    print(station_counts.sort_values().tail(10))
    
     # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()
    print("The most common starting point is {}".format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()
    print("The most common stopping point is {}".format(common_end_station))

       # TO DO: display most frequent combination of start station and end station trip
    common_start_stop = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most common starting and stopping stations are {}".format(common_start_stop))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    while True:
        proceed = input("\nto continue enter y\n")
        if proceed == 'y':
            break 

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    travel_counts = df.groupby('Gender')['Trip Duration'].count()
    print("Trip duration by gender\n {}".format(travel_counts))
    
    tc = np.array(travel_counts)
    for female in tc.flat:
        print(female)
        
    see_plot = input("Would you like to see a plot of gender using trip duration? y or n ")
    if see_plot == 'y':
        tc.plot.bar()
        plt.show()

     # TO DO: display total travel time
    total_travel = df['Trip Duration'].mode()
    print("Longest travel time {}".format(total_travel))

    df['age'] = df['year_start'] - (df['Birth Year'].fillna(method = 'bfill'))
    
    travel_by_age = df.groupby('age')['Trip Duration'].count()
    
    see_plot = input("Would you like to see a plot of user age by trip duration? y or n ")
    if see_plot == 'y':
        travel_by_age.plot.bar()
        plt.show()
    
    print("The average age for users is {} and average duration is for{} minutes".format(df['age'].mean(), df['Trip Duration'].mean()))
    # TO DO: display mean travel time
    travel_mean = df['Trip Duration'].mean()
    print("The average travel time is {} minutes".format(travel_mean/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    while True:
        proceed = input("\nto continue enter y\n")
        if proceed == 'y':
            break 


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("Count of user types: \n{}".format(user_type_count))
    
    user_by_gender = df.groupby('Gender')['User Type'].count()
    print("user gender {}\n".format(user_by_gender))
    
    
    # TO DO: Display counts of gender
    #gender_fill = df['Gender'].fillna(method = 'ffill')   
    gender_counts = df['Gender'].fillna(method = 'ffill').value_counts()
    print("Gender counts \n{}".format(gender_counts))
    
    gender_age = df.groupby('Gender')['age'].count()
    print("Gender by age \n{}".format(gender_age))
    

    # TO DO: Display earliest, most recent, and most common year of birth
    birth_year_earliest = df['Birth Year'].min()
    print("The earliest birth year is {}".format(birth_year_earliest))

    birth_year_recent = df['Birth Year'].max()
    print("The most recent birth year is {}".format(birth_year_recent))

    birth_year_common = df.groupby(['Birth Year']).size().nlargest(1)
    print("The most common year {}".format(birth_year_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
       

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
