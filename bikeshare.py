import time
import pandas as pd
import numpy as np
import datetime

# Dictionary mapping city names to their corresponding CSV file names
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}



def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" for no filter.
        day (str): Name of the day of week to filter by, or "all" for no filter.
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    # Define valid options
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    # Get user input for city
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').strip().lower()
        if city in valid_cities:
            break
        print("Invalid input! Please choose from: Chicago, New York City, or Washington.\n")
    
    # Get user input for month
    while True:
        month = input(
            "\nWhich month would you like to filter by? Type 'all' if you don't want to filter by month.\n"
        ).strip().lower()
        if month in valid_months:
            break
        print("Invalid input. Please enter a valid month (january to june) or 'all'.\n")
    
    # Get user input for day of week
    while True:
        day = input(
            "\nWhich day would you like to see data for? Type 'all' if you don't want to filter by day.\n"
        ).strip().lower()
        if day in valid_days:
            break
        print("Invalid input. Please enter a valid day (e.g., monday) or 'all'.\n")
    
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" for no filter.
        day (str): Name of the day of week to filter by, or "all" for no filter.

    Returns:
        df (DataFrame): Pandas DataFrame containing city data filtered by month and day.
    """
    # Read the CSV file for the selected city
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert 'Start Time' to datetime and extract relevant time information
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()  # Use dt.day_name() for newer pandas versions
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if a specific month is selected
    if month != 'all':
        # Create list of months to convert month name into month number
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    # Filter by day of week if a specific day is selected
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel:
    - Most common month
    - Most common day of week
    - Most common start hour
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    common_day = df['day_of_week'].mode()[0]
    common_hour = df['hour'].mode()[0]

    print(f'Most common month: {common_month}')
    print(f'Most common day of week: {common_day}')
    print(f'Most common start hour: {common_hour}')
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip:
    - Most common start station
    - Most common end station
    - Most frequent combination of start and end station trip
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start = df['Start Station'].mode()[0]
    common_end = df['End Station'].mode()[0]
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print(f'Most common start station: {common_start}')
    print(f'Most common end station: {common_end}')
    print(f'The most popular trip from start to end is: {popular_trip}')
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration:
    - Total travel time
    - Average travel time
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = int(df['Trip Duration'].sum())
    mean_duration = int(df['Trip Duration'].mean())

    print(f'Total travel time: {datetime.timedelta(seconds=total_duration)}')
    print(f'Average travel time: {datetime.timedelta(seconds=mean_duration)}')
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def user_stats(df, city):
    """
    Displays statistics on bikeshare users, including:
    - Counts of user types
    - Counts of gender (if available)
    - Earliest, most recent, and most common year of birth (if available)

    Args:
        df (DataFrame): The DataFrame containing city data.
        city (str): City name (used to check if gender and birth data are available).
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Counts of user types:")
    print(df['User Type'].value_counts())

    # For cities other than Washington, display gender and birth year statistics if available
    if city != 'washington':
        print("\nCounts of gender:")
        print(df['Gender'].value_counts())

        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {recent_year}")
        print(f"Most common year of birth: {common_year}")
    else:
        print("\nNo gender or birth year data available for Washington.")
    
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """
    Displays raw data 5 rows at a time upon user request.

    Args:
        df (DataFrame): The DataFrame containing city data.
    """
    start_row = 0
    while True:
        print(df.iloc[start_row:start_row+5])
        start_row += 5
        
        # Check if there is more data to display
        if start_row >= len(df):
            print("\nNo more raw data to display.")
            break
        
        more = input("\nWould you like to see the next 5 rows of raw data? Enter 'yes' or 'no': ").strip().lower()
        if more != 'yes':
            break

def main():
    """
    Main function to execute the overall flow:
    - Get user filters.
    - Load and filter data.
    - Display raw data upon request.
    - Calculate and display various statistics.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Optionally display raw data
        display_raw_data(df)
        
        # Display statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break

# Entry point for the program
if __name__ == "__main__":
    main()
