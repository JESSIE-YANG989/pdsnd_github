import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_user_input(prompt, valid_choices):
    """
    Helper function to get valid user input.

    Args:
        prompt (str): The prompt to display to the user.
        valid_choices (list): List of valid input choices.

    Returns:
        str: Valid user input.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_choices:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(valid_choices)}\n")

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" for no filter.
        day (str): Name of the day of week to filter by, or "all" for no filter.
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    city = get_user_input('Would you like to see data for Chicago, New York City or Washington?\n', valid_cities)
    month = get_user_input("Which month would you like to filter by? Type 'all' if you don't want to filter by month.\n", valid_months)
    day = get_user_input("Which day would you like to see data for? Type 'all' if you don't want to filter by day.\n", valid_days)
    
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Returns:
        df (DataFrame): Pandas DataFrame containing city data filtered by month and day.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def calculate_stats(df, col_name):
    """
    Calculate the most common value of a given column.

    Args:
        df (DataFrame): DataFrame to analyze.
        col_name (str): The column name to calculate the mode.

    Returns:
        str: Most common value in the column.
    """
    return df[col_name].mode()[0]

def time_stats(df):
    """Calculates and prints the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print(f'Most common month: {calculate_stats(df, "month")}')
    print(f'Most common day of week: {calculate_stats(df, "day_of_week")}')
    print(f'Most common start hour: {calculate_stats(df, "hour")}')
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """Calculates and prints the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(f'Most common start station: {calculate_stats(df, "Start Station")}')
    print(f'Most common end station: {calculate_stats(df, "End Station")}')
    
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'The most popular trip from start to end is: {popular_trip}')
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """Calculates and prints total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = int(df['Trip Duration'].sum())
    mean_duration = int(df['Trip Duration'].mean())

    print(f'Total travel time: {datetime.timedelta(seconds=total_duration)}')
    print(f'Average travel time: {datetime.timedelta(seconds=mean_duration)}')
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def user_stats(df, city):
    """Calculates and prints statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Counts of user types:")
    print(df['User Type'].value_counts())

    if city != 'washington':
        print("\nCounts of gender:")
        print(df['Gender'].value_counts())

        print(f"\nEarliest year of birth: {int(df['Birth Year'].min())}")
        print(f"Most recent year of birth: {int(df['Birth Year'].max())}")
        print(f"Most common year of birth: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nNo gender or birth year data available for Washington.")
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    start_row = 0
    while True:
        print(df.iloc[start_row:start_row+5])
        start_row += 5
        
        if start_row >= len(df):
            print("\nNo more raw data to display.")
            break
        
        more = input("\nWould you like to see the next 5 rows of raw data? Enter 'yes' or 'no': ").strip().lower()
        if more != 'yes':
            break

def main():
    """Main function to execute the overall flow."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
