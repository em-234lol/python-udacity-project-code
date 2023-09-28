import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please choose a valid city.')

    month = input('Which month? January, February, March, April, May, June, or all? ').lower()
    day = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ').lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    try:
        # Load data from the specified city
        df = pd.read_csv(CITY_DATA[city])

        # Convert 'Start Time' column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract month and day of week from 'Start Time' to create new columns
        df['Month'] = df['Start Time'].dt.month
        df['Day of Week'] = df['Start Time'].dt.day_name()

        # Filter by month if applicable
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month_index = months.index(month) + 1
            df = df[df['Month'] == month_index]

        # Filter by day of week if applicable
        if day != 'all':
            df = df[df['Day of Week'] == day.title()]

        return df
    except FileNotFoundError:
        print(f"Error: The data file for {city} was not found.")
        exit()

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['Month'].mode()[0]
    print('Most Common Month:', common_month)

    # Display the most common day of week
    common_day = df['Day of Week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    # Display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    common_start_hour = df['Start Hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)

    # Display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_station_combination = df['Station Combination'].mode()[0]
    print('Most Common Station Combination:', common_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time, 'seconds')

    # Display average travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', average_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_info(df, city):
    print('\nCalculating User Info...\n')
    start_time = time.time()

    # Display counts of each user type
    user_type_counts = df['User Type'].value_counts()
    print('User Type Counts:\n', user_type_counts)

    if city in ['chicago', 'new york city']:
        # Display counts of each gender
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts:\n', gender_counts)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Earliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    print("Explore US Bikeshare Data\n")
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print("\nData analysis for {}:\n".format(city.title()))

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_info(df, city)

        # Ask the user if they want to view raw data
        raw_data_display = input("\nWould you like to view raw data? Enter 'yes' or 'no': ").lower()
        if raw_data_display == 'yes':
            start_idx = 0
            chunk_size = 5  # Display 5 rows at a time

            while start_idx < len(df):
                print(df.iloc[start_idx : start_idx + chunk_size])
                start_idx += chunk_size
                more_data = input("\nView more raw data? Enter 'yes' or 'no': ").lower()
                if more_data != 'yes':
                    break

        restart = input("\nWould you like to restart? Enter 'yes' or 'no': ")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

    