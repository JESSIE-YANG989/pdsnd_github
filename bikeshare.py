import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
        if city in cities:
            break
        else: 
            print('Invalid input! Please enter one of the following cities: chicago, new york city, washington.\n')

    # Get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input("\nWhich month would you like to filter by?\nType 'all' if you don't want to filter by month.\n").lower()
        if month in months:
            break
        else:
            print('Invalid input. Please enter a valid month or "all".\n')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
        day = input("Which day would you like to see data for?\nType 'all' if you don't want to filter by day.\n").lower()
        if day in days:
            break
        else: 
            print("Invalid input. Please enter a valid day or 'all'.\n")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october','november', 'december']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    comm_mth = df['month'].mode()[0]
    print('Most common month: {}'.format(comm_mth))

    # Most common day of week
    comm_dow = df['day_of_week'].mode()[0]
    print('Most common day of week: {}'.format(comm_dow))

    # Most common start hour
    comm_hour = df['hour'].mode()[0]
    print('Most common start hour: {}'.format(comm_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    comm_start = df['Start Station'].mode()[0] 
    print('Most common start station: {}'.format(comm_start))

    # Most commonly used end station
    comm_end = df['End Station'].mode()[0]
    print('Most common end station: {}'.format(comm_end))

    # Most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most popular trip from start to end is {}".format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_time = int(df['Trip Duration'].sum())  # Convert to int
    print('Total travel time: {}'.format(str(datetime.timedelta(seconds=total_time))))

    # Mean travel time
    mean_time = int(df['Trip Duration'].mean())  # Convert to int
    print('Average travel time: {}'.format(str(datetime.timedelta(seconds=mean_time))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    if city != 'washington':
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("\nThe counts grouped by users' gender is: {}".format(gender_count))

        # Display earliest, most recent, and most common year of birth
        earliest_bday = df['Birth Year'].min()
        recent_bday = df['Birth Year'].max()
        comm_bday = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth: {}, Most recent year of birth: {}, Most common year of birth: {}".format(earliest_bday, recent_bday, comm_bday))
    else: 
        print("\nThere is no birth data or gender information for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_raw_data(df):
    """Displays raw data 5 lines at a time upon user request."""
    index = 0
    while True:
        # Display the next 5 rows
        print(df.iloc[index:index + 5])
        
        # Update the index for the next 5 rows
        index += 5
        
        # Ask if the user wants to see more data
        show_more = input("\nWould you like to see the next 5 rows of raw data? Enter 'yes' or 'no': ").lower()
        
        if show_more != 'yes':
            break
        
        # If all rows are shown, break out of the loop
        if index >= len(df):
            print("\nNo more raw data to display.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
#publish on github 20250205
if __name__ == "__main__":
    main()

