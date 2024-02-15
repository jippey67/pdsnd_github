import time
import pandas as pd
import calendar

DEBUG = False

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_keyboard_input(question_set):
    """
    - asks the user to answer the questions in ARGUMENT question_set
    - converts the answer to lower case
    - checks against valid answers in the acceptance_list
    - re-solicit input when answer is invalid
    - returns a dictionary with values for the following keys:
        city - name of the city to analyze
        month - name of the month to filter by, or "none" to apply no month filter
        day - number of the day of week to filter by, or "none" to apply no day filter
    """
    if DEBUG:
        answer_dict = {
            'city': 'washington',
            'month': 'mar',
            'day': '4'
        }
    else:
        answer_dict = {}
        for key, value in question_set.items():
            success = False
            while not success:
                answer = input(value['q']).lower()
                if answer in value['val']:
                    success = True
                else:
                    print('This answer is not valid. Please Try again!')
            answer_dict[key] = answer
    return answer_dict

def get_filters():
    """
    - asks user to specify a city, month, and day to analyze.
    - returns a dictionary with (string) values for the following keys:
        city - name of the city to analyze
        month - name of the month to filter by, or "none" to apply no month filter
        day - number of the day of week to filter by, or "none" to apply no day filter
    """
    question_set = {
        'city': {'q': 'What city do you want to analyze? Chicago, New York or Washington? Type the city name.\n', 'val':['chicago', 'new york', 'washington']},
        'month': {'q': 'Do you want to filter on Month? If so, type Jan, Feb, Mar, Apr, May, Jun. Otherwise type "none".\n', 'val': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'none']},
        'day': {'q': 'Do you want to filter on Week day? If so, type the day number (Sunday = 0). Otherwise type "none".\n', 'val': ['0', '1', '2', '3', '4', '5', '6', 'none']}
    }

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    filters = get_keyboard_input(question_set)
    print('-'*40)
    return filters


def load_data(filters):
    """
    -loads data for the specified city and filters by month and day if applicable.
    Args: dictionary with (string) values for the following keys:
        city - name of the city to analyze
        month - name of the month to filter by, or "all" to apply no month filter
        day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[filters['city']])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    # filter by month if applicable
    if filters['month'] != 'none':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(filters['month']) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if filters['day'] != 'none':
        # filter by day of week to create the new dataframe
        day = int(filters['day'])
        df = df[df['day_of_week'] == day]
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = (df['month']).mode()[0]
    print(f'The most common month in the selection is: {calendar.month_name[month_mode]}')

    # display the most common day of week
    day_mode = (df['day_of_week']).mode()[0]
    print(f'The most common week day in the selection is: {calendar.day_name[day_mode-1]}')

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    hour_mode = (df['hour']).mode()[0]
    print(f'The most common starting hour in the selection is: {hour_mode}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print(f'The most common start station in the selection is: {start_station_mode}')

    # display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print(f'The most common end station in the selection is: {end_station_mode}')

    # display most frequent combination of start station and end station trip
    df['route'] = df[['Start Station', 'End Station']].agg(' --> '.join, axis=1)
    route_mode = df['route'].mode()[0]
    print(f'The most common route in the selection is: {route_mode}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time in the selection is: {round(tot_travel_time)} seconds')

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print(f'The total travel time in the selection is: {round(avg_travel_time)} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, selection_criteria):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types en gender
    availability_check = selection_criteria['city']

    user_type_counts = df[['Start Time', 'User Type']].groupby('User Type', as_index=False).count().rename(columns={'Start Time': 'Occurences'})
    print('The number of the various user types in the selection is: ')
    print(user_type_counts, '\n')

    # Display counts of gender and earliest, most recent, and most common year of birth
    if availability_check == 'washington':
        print(f'For {availability_check.capitalize()} no gender and birth year information exists')
    else:
        gender_counts = df[['Gender', 'User Type']].groupby('Gender', as_index=False).count().rename(columns={'User Type': 'Occurences'})
        print('The number of Male/Female in the selection is: ')
        print(gender_counts, '\n')

        yob_min = round(df['Birth Year'].min())
        yob_max = round(df['Birth Year'].max())
        yob_mode = round(df['Birth Year'].mode()[0])
        print(f'The earliest birth year in the selection is: {yob_min}')
        print(f'The most recent birth year in the selection is: {yob_max}')
        print(f'The most common birth year in the selection is: {yob_mode}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_y_n_from_keyboard(question):
    """Helper function to obtain yes/no answers from the keyboard, to the question in ARG question"""
    success = False
    while not success:
        selector = input(question).lower()
        if selector in ['yes', 'no']:
            success = True
        else:
            print('Please answer yes or no. Try again!')
    return selector

def main():
    while True:
        selection_criteria = get_filters()
        df = load_data(selection_criteria)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, selection_criteria)

        total_rows = df.shape[0]
        rows_displayed = 0
        pd.set_option('display.max_columns', None)

        selector = get_y_n_from_keyboard('Do you want to see 5 lines of data? Enter yes or no.\n')
        if selector == 'yes':
            print(df[rows_displayed:rows_displayed+5])
            rows_displayed += 5
            display_more = True
            while display_more:
                print(f'There are {total_rows - rows_displayed} more lines available.')
                selector = get_y_n_from_keyboard('Do you want to see some more lines of data? Enter yes or no.\n')
                if selector == 'yes':
                    print(df[rows_displayed:rows_displayed + 5])
                    rows_displayed += 5
                else:
                    display_more = False

        restart = get_y_n_from_keyboard('\nWould you like to restart? Enter yes or no.\n')
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()

