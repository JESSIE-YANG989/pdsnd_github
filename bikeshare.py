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
        city (str): name of the city to analyze (chicago, new york city, or washington)
        month (str): name of the month to filter by, or "all" to apply no month filter
        day (str): name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city (chicago, new york city, washington)
    while True:
        # List of available cities
        cities = ['chicago', 'new york city', 'washington']
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
        if city in cities:
            break
        else: 
            print('Invalid input! Please enter one of the following cities: chicago, new york city, washington.\n')

    # Get user input for month (all, january, february, ... , june)
    while True:
        # List of available months; "all" means no filter
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input("\nWhich month would you like to filter by?\nType 'all' if you don't want to filter by month.\n").lower()
        if month in months:
            break
        else:
            print('Invalid input. Please enter a valid month or "all".\n')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        # List of available days; "all" means no filter
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
        day = input("Which day would you like to see data for?\nType 'all' if you don't want to filter by day.\n").lower()
        if day in days:
            break
        else: 
            print("Invalid input. Please enter a valid day or 'all'.\n")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): name of the city to analyze
        month (str): name of the month to filter by, or "all" to apply no month filter
        day (str): name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df (DataFrame): Pandas DataFrame containing city data filtered by month and day
    """
    # Read the CSV file for the selected city
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month, day of week, and hour from 'Start Time' for further analysis
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name  # Note: in newer versions of pandas, use dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month if applicable
    if month != 'all':
        # List of all months to get the corresponding month number
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']
        # Convert month name to month number (e.g., january -> 1)
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    # Filter by day of week if applicable
    if day != 'all':
        # Capitalize the first letter to match the format in the DataFrame (e.g., 'monday' -> 'Monday')
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

    # Calculate the most common month
    comm_mth = df['month'].mode()[0]
    print('Most common month: {}'.format(comm_mth))

    # Calculate the most common day of week
    comm_dow = df['day_of_week'].mode()[0]
    print('Most common day of week: {}'.format(comm_dow))

    # Calculate the most common start hour
    comm_hour = df['hour'].mode()[0]
    print('Most common start hour: {}'.format(comm_hour))

    # Display the time taken to perform these calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip:
    - Most common start station
    - Most common end station
    - Most frequent combination of start station and end station trip
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculate the most common start station
    comm_start = df['Start Station'].mode()[0] 
    print('Most common start station: {}'.format(comm_start))

    # Calculate the most common end station
    comm_end = df['End Station'].mode()[0]
    print('Most common end station: {}'.format(comm_end))

    # Calculate the most frequent combination of start and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most popular trip from start to end is {}".format(popular_trip))

    # Display the time taken to perform these calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration:
    - Total travel time
    - Average travel time
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time (in seconds) and convert to a timedelta format for better readability
    total_time = int(df['Trip Duration'].sum())
    print('Total travel time: {}'.format(str(datetime.timedelta(seconds=total_time))))

    # Calculate mean travel time (in seconds) and convert to a timedelta format
    mean_time = int(df['Trip Duration'].mean())
    print('Average travel time: {}'.format(str(datetime.timedelta(seconds=mean_time))))

    # Display the time taken to perform these calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df, city):
    """
    Displays statistics on bikeshare users, including:
    - Counts of user types
    - Counts of gender (if available)
    - Earliest, most recent, and most common year of birth (if available)

    Args:
        df (DataFrame): The DataFrame containing city data
        city (str): City name (used to check if gender and birth data are available)
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # For cities other than Washington, display gender and birth year statistics
    if city != 'washington':
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("\nThe counts grouped by users' gender is: {}".format(gender_count))

        # Display earliest, most recent, and most common year of birth
        earliest_bday = df['Birth Year'].min()
        recent_bday = df['Birth Year'].max()
        comm_bday = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth: {}, Most recent year of birth: {}, Most common year of birth: {}".format(
            earliest_bday, recent_bday, comm_bday))
    else: 
        # Washington data does not include gender or birth year information
        print("\nThere is no birth data or gender information for Washington.")

    # Display the time taken to perform these calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    """
    Displays raw data 5 rows at a time upon user request.

    Args:
        df (DataFrame): The DataFrame containing city data
    """
    index = 0
    while True:
        # Display 5 rows of raw data starting from the current index
        print(df.iloc[index:index + 5])
        
        # Update the index for the next 5 rows
        index += 5
        
        # Ask the user if they want to see the next 5 rows
        show_more = input("\nWould you like to see the next 5 rows of raw data? Enter 'yes' or 'no': ").lower()
        
        if show_more != 'yes':
            break
        
        # If all rows have been displayed, exit the loop
        if index >= len(df):
            print("\nNo more raw data to display.")
            break

def main():
    """
    Main function to execute the overall flow:
    - Get user filters
    - Load and filter data
    - Display raw data upon request
    - Calculate and display various statistics
    """
    while True:
        # Get filter criteria from the user
        city, month, day = get_filters()
        # Load data based on the specified filters
        df = load_data(city, month, day)
        # Display raw data if requested by the user
        display_raw_data(df)
        # Display time-related statistics
        time_stats(df)
        # Display station statistics
        station_stats(df)
        # Display trip duration statistics
        trip_duration_stats(df)
        # Display user statistics
        user_stats(df, city)

        # Ask the user if they would like to restart the analysis
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# Program entry point: execute main() when the script is run directly
if __name__ == "__main__":
    main()
