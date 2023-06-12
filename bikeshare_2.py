"""Udacity Project #2 Bikeshare

    Returns:
        Output for given questions asked
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

MONTHS = {'January': 1,
          'February':2,
          'March':3,
          'April':4,
          'May':5,
          'June':6 }


DAYS_OF_WEEK = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

def convert_hours_to_time(hour):
    if(hour < 12):
        string_hour = "%s:00 A.M." % str(hour)
    elif(hour > 12 and hour < 24):
        new_hour = hour - 12
        string_hour = "%s:00 P.M." % str(new_hour)
    else:
        string_hour = str(hour)
    return string_hour

def get_key(val, dictionary):
   
    for key, value in dictionary.items():
        if val == value:
            return key
 
    return "key doesn't exist"

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to look into?  Chicago, New York City, or Washington?\n")
        city = city.lower()
        city = str.title(city)
        if city not in CITY_DATA:
            print("Incorrect value chosen.  Please try again\n")
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to look into? %s or  type 'All' for all months\n" % (', '.join(MONTHS.keys())))
        month = month.lower()
        month = str.title(month)
        if month not in MONTHS and month != 'All':
            print("Incorrect value chosen.  Please try again\n")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week would you like to look into? %s or type 'All' for all days of the week\n" % (', '.join(DAYS_OF_WEEK)))
        day = day.lower()
        day = str.title(day)
        if day not in DAYS_OF_WEEK and day != 'All':
            print("Incorrect value chosen.  Please try again\n")
            continue
        else:
            break
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
    df = pd.read_csv(CITY_DATA[city])
    # convert the start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # create a new column for the Month
    df['month'] = df['Start Time'].dt.month
    # create a new column for the day of the week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # now lets filter if needed
    if(month != 'All'):
        df = df[df['month'] == MONTHS[month]]
        
    if(day != 'All'):
        df = df[df['day_of_week'] == day]
    
    print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    month_by_name = get_key(common_month, MONTHS)
    print("The most common month is: \n", month_by_name)
    
    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the weeks is: \n", common_day_of_week)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_of_day = convert_hours_to_time(df['hour'].mode()[0])
    print("The most common hour is: \n", hour_of_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print("The most common start station is: \n", start_station)

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print("The most common end station is: \n", end_station)

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most common used start and end station trips is: \n", combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time was: %s seconds or %s hours \n" % (total_travel_time, total_travel_time/3600))

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("Total travel time was: %s seconds or %s hours \n" % (mean_duration, mean_duration/3600))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Types of user stats \n %s \n" %(user_types))
    
    try:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print("Gender stats \n %s \n" % (gender))

        # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        recent_year_of_birth = df['Birth Year'].max()
        common_year_of_birth = df['Birth Year'].value_counts().idxmax()
        print("The earliest birth year is %s \nThe most recent birth year is %s \nThe most common birth year is %s" %(int(earliest_year_of_birth), int(recent_year_of_birth), int(common_year_of_birth)))
    except:
        print("Data was missing for Gender and/or Birth years")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # prompt the user if they would like to see the lines of data
    counter = 5
    while True:
        user_input = input("Would you like to see 5 lines of raw data?\n")
        if user_input.lower() == 'yes':
            print(df[counter:counter+5])
            counter = counter + 5
            continue 
        elif user_input.lower() == 'no':
            break
        else:
            print("Please type 'yes' or 'no'")
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
