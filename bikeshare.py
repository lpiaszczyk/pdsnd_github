import time

import numpy as np
import pandas as pd
from simple_term_menu import TerminalMenu

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Which city data would you like to analyze?')
    cities = list(CITY_DATA.keys())
    options = [cities[0], cities[1], cities[2], 'All Cities']
    selected = show_term_menu(options)
    print(f"You have selected {options[selected]}!")
    city = options[selected]
    if city == 'All Cities':
        print("Please keep in mind that some data may be not available for all cities. Some statistics may be incorrect.")

    print('Select month for data analysis:')
    options = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    selected = show_term_menu(options)
    print(f"We'll show data for {options[selected]}")
    month = options[selected]

    print('Select day for data analysis:')
    options = ['Monday', 'Tuesday', 'Wednesday',
               'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
    selected = show_term_menu(options)
    print(f"We'll show data for {options[selected]}")
    day = options[selected]

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
    if city != 'All Cities':
        df = pd.read_csv(CITY_DATA[city])
    else:
        df_chicago = pd.read_csv(CITY_DATA['Chicago'])
        df_newYork = pd.read_csv(CITY_DATA['New York City'])
        df_washington = pd.read_csv(CITY_DATA['Washington'])
        # cast washington trip duration to the same type as in other cities
        df_washington['Trip Duration'] = df_washington['Trip Duration'].astype(
            'int')
        df = df_chicago.merge(df_newYork, how='left').merge(
            df_washington, how='left')
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"The most popular hour was: {popular_hour}")
    df['day'] = df['Start Time'].dt.day_name()

    popular_day = df['day'].mode()[0]
    print(f"The most popular day was: {popular_day}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if {'Start Station', 'End Station'}.issubset(df.columns):
        popular_start = df['Start Station'].mode()[0]
        print(f"The most popular start station was: {popular_start}")

        popular_end = df['End Station'].mode()[0]
        print(f"The most popular end station was: {popular_end}")

        df['start_stop'] = df['Start Station'] + " -> " + df['End Station']
        popular_start_stop = df['start_stop'].mode()[0]
        print(f"The most popular route was: {popular_start_stop}")
    else:
        print("Unfortunatelly, we don't have data related to routes for that city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if 'Trip Duration' in df:
        total_time = df['Trip Duration'].sum()
        print(
            f"Total trip duration in selected city and time range was {total_time} minutes or {total_time / 60} hours")

        total_mean_time = df['Trip Duration'].mean()
        print(
            f"Mean trip duration in selected city and time range was {total_mean_time} minutes or {total_mean_time / 60} hours")
    else:
        print("Unfortunately, we don't have data regaring Trip Duration for selected city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if 'User Type' in df:
        count_types = df['User Type'].count()
        types_grouped = df['User Type'].value_counts()
        print(
            f"In selected time range, we registered {count_types} users that used service")
        print(
            f"Within that, there were {types_grouped['Subscriber']} subscribers and {types_grouped['Customer']} customers.")
    else:
        print("Unfortunately, we don't have data regarding User Types for selected city")

    if 'Gender' in df:
        gender_grouped = df['Gender'].dropna().value_counts()
        gender_nan = df['Gender'].isna().sum()
        print(
            f"In selected range, there were {gender_grouped['Male']} male and {gender_grouped['Female']} female users")
        print(f"{gender_nan} decided not to share their gender.")
    else:
        print("Unfortunately, we don't have data regarding users Gender for selected city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_term_menu(options):
    """
    Show terminal menu to select option

    Args:
        (list) options - a list of options that will be presented

    Returns:
        (int) index of option selected from provided list
    """
    terminal_menu = TerminalMenu(options)
    return terminal_menu.show()


def show_raw_data(df):
    """
    Allows to print raw data from dataframe
    Args:
    (DataFrame) df - supplied dataframe that will be printed
    """
    print('Would you like to see first 5 rows of raw data?')
    start = 0
    end = 5
    options = ["Yes", "No"]
    while (True):
        selected = show_term_menu(options)
        if (options[selected] == 'Yes'):
            if end > df.index.size:
                print(df[:-(df.index.size - end)].to_markdown())
                print("That's the end of data")
                break
            print(df[start:end].to_markdown())
            start += 5
            end += 5
            print('Would you like to see more?')
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        print('\nWould you like to restart?')
        options = ['Yes', 'No']
        selected = show_term_menu(options)
        if selected == 1:
            break


if __name__ == "__main__":
    main()
