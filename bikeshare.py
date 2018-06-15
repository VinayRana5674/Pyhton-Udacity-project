
In [1]:
## import all necessary packages and functions.
import csv # read and write csv files
from datetime import datetime # operations to parse dates
from pprint import pprint # use to print data structures like dictionaries in
                          # a nicer way than the base print function.
In [2]:
def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))
    
    with open(filename, 'r') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)
        
        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        first_trip = next(trip_reader)
        
        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##
        pprint(first_trip)
        
        
    # output city name and first trip for later testing
    return (city, first_trip)


# list of files for each city
data_files = ['./data/NYC-CitiBike-2016.csv',
              './data/Chicago-Divvy-2016.csv',
              './data/Washington-CapitalBikeshare-2016.csv',]


# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip
City: NYC
OrderedDict([('tripduration', '839'),
             ('starttime', '1/1/2016 00:09:55'),
             ('stoptime', '1/1/2016 00:23:54'),
             ('start station id', '532'),
             ('start station name', 'S 5 Pl & S 4 St'),
             ('start station latitude', '40.710451'),
             ('start station longitude', '-73.960876'),
             ('end station id', '401'),
             ('end station name', 'Allen St & Rivington St'),
             ('end station latitude', '40.72019576'),
             ('end station longitude', '-73.98997825'),
             ('bikeid', '17109'),
             ('usertype', 'Customer'),
             ('birth year', ''),
             ('gender', '0')])

City: Chicago
OrderedDict([('trip_id', '9080545'),
             ('starttime', '3/31/2016 23:30'),
             ('stoptime', '3/31/2016 23:46'),
             ('bikeid', '2295'),
             ('tripduration', '926'),
             ('from_station_id', '156'),
             ('from_station_name', 'Clark St & Wellington Ave'),
             ('to_station_id', '166'),
             ('to_station_name', 'Ashland Ave & Wrightwood Ave'),
             ('usertype', 'Subscriber'),
             ('gender', 'Male'),
             ('birthyear', '1990')])

City: Washington
OrderedDict([('Duration (ms)', '427387'),
             ('Start date', '3/31/2016 22:57'),
             ('End date', '3/31/2016 23:04'),
             ('Start station number', '31602'),
             ('Start station', 'Park Rd & Holmead Pl NW'),
             ('End station number', '31207'),
             ('End station', 'Georgia Ave and Fairmont St NW'),
             ('Bike number', 'W20842'),
             ('Member Type', 'Registered')])

In [3]:
def duration_in_mins(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.
    
    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds. 
    
    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """
         
    if city == 'NYC':
        duration = float(datum['tripduration']) / 60
    elif city == 'Chicago':
        duration = float(datum['tripduration']) / 60
    else: 
        duration = float(datum['Duration (ms)']) / 60000
    return duration

# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 13.9833,
         'Chicago': 15.4333,
         'Washington': 7.1231}

for city in tests:
    assert abs(duration_in_mins(example_trips[city], city) - tests[city]) < .001
In [4]:
def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.
    
    Remember that NYC includes seconds, while Washington and Chicago do not.
    
    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    
    if city == 'Chicago':
        datetime_object = datetime.strptime((datum['starttime']), '%m/%d/%Y %H:%M')
        month = datetime_object.month
        hour = datetime_object.hour
        day_of_week = datetime_object.strftime("%A")
        
    elif city == 'NYC':
        datetime_object = datetime.strptime((datum['starttime']), '%m/%d/%Y %H:%M:%S')
        month = datetime_object.month
        hour = datetime_object.hour
        day_of_week = datetime_object.strftime("%A") 
    
    else: 
        datetime_object = datetime.strptime((datum['Start date']), '%m/%d/%Y %H:%M')
        month = datetime_object.month
        hour = datetime_object.hour
        day_of_week = datetime_object.strftime("%A")
    
    return (month, hour, day_of_week)


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': (1, 0, 'Friday'),
         'Chicago': (3, 23, 'Thursday'),
         'Washington': (3, 22, 'Thursday')}

for city in tests:
    assert time_of_trip(example_trips[city], city) == tests[city]
In [5]:
def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.
    
    Remember that Washington has different category names compared to Chicago
    and NYC. 
    """
    if city == 'Chicago':
        user_type = datum['usertype']
    elif city == 'NYC':
        user_type = datum['usertype']
    else: 
        temp = datum['Member Type']
        if temp == 'Registered':
            user_type = 'Subscriber'
        else:
            user_type = 'Customer'    
    return user_type


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 'Customer',
         'Chicago': 'Subscriber',
         'Washington': 'Subscriber'}

for city in tests:
    assert type_of_user(example_trips[city], city) == tests[city]
Question 3b: Now, use the helper functions you wrote above to create a condensed data file for each city consisting only of the data fields indicated above. In the /examples/ folder, you will see an example datafile from the Bay Area Bike Share before and after conversion. Make sure that your output is formatted to be consistent with the example file.

In [6]:
def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.
    
    HINT: See the cell below to see how the arguments are structured!
    """
    
    with open(out_file, 'w') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']        
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()
        
        ## TODO: set up csv DictReader object ##
        trip_reader = csv.DictReader(f_in)

        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            new_point = {}

            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            new_point['duration'] = duration_in_mins(row, city)
            new_point['month'], new_point['hour'], new_point['day_of_week'] = time_of_trip(row, city)
            new_point['user_type'] = type_of_user(row, city)

            ## TODO: write the processed information to the output file.     ##
            ## see https://docs.python.org/3/library/csv.html#writer-objects ##
            trip_writer.writerow(new_point)
In [7]:
# Run this cell to check your work
city_info = {'Washington': {'in_file': './data/Washington-CapitalBikeshare-2016.csv',
                            'out_file': './data/Washington-2016-Summary.csv'},
             'Chicago': {'in_file': './data/Chicago-Divvy-2016.csv',
                         'out_file': './data/Chicago-2016-Summary.csv'},
             'NYC': {'in_file': './data/NYC-CitiBike-2016.csv',
                     'out_file': './data/NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])
City: Washington
OrderedDict([('duration', '7.123116666666666'),
             ('month', '3'),
             ('hour', '22'),
             ('day_of_week', 'Thursday'),
             ('user_type', 'Subscriber')])

City: Chicago
OrderedDict([('duration', '15.433333333333334'),
             ('month', '3'),
             ('hour', '23'),
             ('day_of_week', 'Thursday'),
             ('user_type', 'Subscriber')])

City: NYC
OrderedDict([('duration', '13.983333333333333'),
             ('month', '1'),
             ('hour', '0'),
             ('day_of_week', 'Friday'),
             ('user_type', 'Customer')])

In [8]:
def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        # initialize count variables
        n_subscribers = 0
        n_customers = 0
        
        # tally up ride types
        for row in reader:
            if row['user_type'] == 'Subscriber':
                n_subscribers += 1
            else:
                n_customers += 1
        
        # compute total number of rides
        n_total = n_subscribers + n_customers
        
        # return tallies as a tuple
        return(n_subscribers, n_customers, n_total)
    
def proportion_users(filename):
    n_subscribers, n_customers, n_total = number_of_trips(filename)
    
    proportion_of_subscribers = round((n_subscribers / n_total) * 100, 2)
    proportion_of_customers = round((n_customers / n_total) * 100, 2)
    
    return (proportion_of_subscribers, proportion_of_customers)
In [9]:
## Modify this and the previous cell to answer Question 4a. Remember to run ##
## the function on the cleaned data files you created from Question 3.      ##

data_file = './examples/BayArea-Y3-Summary.csv'
print(number_of_trips(data_file))

data_file_NYC = './data/NYC-2016-Summary.csv'

data_file_Washington = './data/Washington-2016-Summary.csv'

data_file_Chicago = './data/Chicago-2016-Summary.csv'

tempo = proportion_users(data_file_NYC)
print("NYC: {}".format(number_of_trips(data_file_NYC)))
print("Proportion of Subscribers in NYC: {}%  Proportion of Customers in NYC: {}%\n".format(tempo[0], tempo[1]))

tempo = proportion_users(data_file_Washington)
print("Washington: {}".format(number_of_trips(data_file_Washington)))
print("Proportion of Subscribers in Washington: {}%  Proportion of Customers in Washington: {}%\n".format(tempo[0], tempo[1]))

tempo = proportion_users(data_file_Chicago)
print("Chicago: {}".format(number_of_trips(data_file_Chicago)))
print("Proportion of Subscribers in Chicago: {}%  Proportion of Customers in Chicago: {}%\n".format(tempo[0], tempo[1]))
(5666, 633, 6299)
NYC: (245896, 30902, 276798)
Proportion of Subscribers in NYC: 88.84%  Proportion of Customers in NYC: 11.16%

Washington: (51753, 14573, 66326)
Proportion of Subscribers in Washington: 78.03%  Proportion of Customers in Washington: 21.97%

Chicago: (54982, 17149, 72131)
Proportion of Subscribers in Chicago: 76.23%  Proportion of Customers in Chicago: 23.77%


In [10]:
## Use this and additional cells to answer Question 4b.                 ##
##                                                                      ##
## HINT: The csv module reads in all of the data as strings, including  ##
## numeric values. You will need a function to convert the strings      ##
## into an appropriate numeric type before you aggregate data.          ##
## TIP: For the Bay Area example, the average trip length is 14 minutes ##
## and 3.5% of trips are longer than 30 minutes.                        ##

def avg_trip_length(filename):
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        total_trip_length = 0
        number_long_trips = 0
        
        for row in reader:
            total_trip_length += float(row['duration'])
            if float(row['duration']) > 30:
                number_long_trips += 1
        total_trips = number_of_trips(filename)
        
        avg_trip = int(total_trip_length / total_trips[2]) 
        proportion = (number_long_trips/total_trips[2]) * 100
        
    return avg_trip, round(proportion, 1)  

data_file_Washington = './data/Washington-2016-Summary.csv'
temp = avg_trip_length(data_file_Washington)
print("Average trip length Washington: {}, Proportion of long trips: {}".format(temp[0], temp[1]))

data_file_Chicago = './data/Chicago-2016-Summary.csv'
temp = avg_trip_length(data_file_Chicago)
print("Average trip length Chicago: {}, Proportion of long trips: {}".format(temp[0], temp[1]))

data_file_NYC = './data/NYC-2016-Summary.csv'
temp = avg_trip_length(data_file_NYC)
print("Average trip length NYC: {}, Proportion of long trips: {}".format(temp[0], temp[1]))

## Use this and additional cells to answer Question 4c. If you have    ##
## not done so yet, consider revising some of your previous code to    ##
## make use of functions for reusability.                              ##
##                                                                     ##
## TIP: For the Bay Area example data, you should find the average     ##
## Subscriber trip duration to be 9.5 minutes and the average Customer ##
## trip duration to be 54.6 minutes. Do the other cities have this     ##
## level of difference?                                                ##

def answer4c(filename):
    with open(filename, 'r') as f_in:
        Reader = csv.DictReader(f_in)
        
        subscriber_duration = 0
        customer_duration = 0
        
        for row in Reader:
            if row['user_type'] == 'Subscriber':
                subscriber_duration += float(row['duration'])
            else:
                customer_duration += float(row['duration'])
                
        total_trips = number_of_trips(filename)
        
        avg_trip_duration_subscribers = (subscriber_duration / total_trips[0])
        
        avg_trip_duration_customers = (customer_duration / total_trips[1])
    
    return round(avg_trip_duration_subscribers, 1),  round(avg_trip_duration_customers, 1)
                

    
data_file_NYC = './data/NYC-2016-Summary.csv'
temp = answer4c(data_file_NYC)
print("City Selected NYC, Average trip duration Subscribers: {} ; Average trip duration Customers: {} ".format(temp[0], temp[1]))

In [12]:
# load library
import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
%matplotlib inline 

# example histogram, data taken from bay area sample
data = [ 7.65,  8.92,  7.42,  5.50, 16.17,  4.20,  8.98,  9.62, 11.48, 14.33,
        19.02, 21.53,  3.90,  7.97,  2.62,  2.67,  3.08, 14.40, 12.90,  7.83,
        25.12,  8.30,  4.93, 12.43, 10.60,  6.17, 10.88,  4.78, 15.15,  3.53,
         9.43, 13.32, 11.72,  9.85,  5.22, 15.10,  3.95,  3.17,  8.78,  1.88,
         4.55, 12.68, 12.38,  9.78,  7.63,  6.45, 17.38, 11.90, 11.52,  8.63,]
plt.hist(data)
plt.title('Distribution of Trip Durations')
plt.xlabel('Duration (m)')
plt.show()


In [13]:
## Use this and additional cells to collect all of the trip times as a list ##
## and then use pyplot functions to generate a histogram of trip times.     ##

def plot_graph(filename,city):
    with open(filename, 'r') as f_in:
        Reader = csv.DictReader(f_in)
        
        data = []
        
        for row in Reader:
            data.append(round(float(row['duration']), 2))
    plt.hist(data)
    plt.title('Distribution of Trip Durations for ' + city)
    plt.xlabel('Duration (m)')
    plt.show()
            
data_file_Washington = './data/Washington-2016-Summary.csv'
plot_graph(data_file_Washington, 'Washington')


In [18]:
## Use this and additional cells to answer Question 5. ##
import numpy as np
def plot_subscriber(filename):
    
    with open(filename, 'r') as f_in:
        Reader = csv.DictReader(f_in)
        data = []
        
        for row in Reader:
            if row['user_type'] == 'Subscriber':
                data.append(round(float(row['duration']), 2))
                
    plt.hist(data, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
    plt.xticks(np.arange(0, 76, 5.0))
    plt.title('Plot of Trip Durations of Subscribers in Washington')
    plt.xlabel('Duration (m)')
    plt.show()
            
data_file_Washington = './data/Washington-2016-Summary.csv'
plot_subscriber(data_file_Washington)

In [19]:
def plot_customer(filename):
    
    with open(filename, 'r') as f_in:
        Reader = csv.DictReader(f_in)
        data = []
        
        for row in Reader:
            if row['user_type'] == 'Customer':
                data.append(round(float(row['duration']), 2))
    
    plt.hist(data, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
    plt.xticks(np.arange(0, 76, 5.0))
    plt.title('Plot of Trip Durations of Customers in Washington')
    plt.xlabel('Duration (m)')
    plt.show()
            
data_file_Washington = './data/Washington-2016-Summary.csv'
plot_customer(data_file_Washington)



In [21]:
## Use this and additional cells to continue to explore the dataset. ##
## Once you have performed your exploration, document your findings  ##
## in the Markdown cell above.         

import calendar
def per_day_analysis(filename, usertype):
    if usertype not in ['Subscriber', 'Customer']:
        return "User type does not exist !"
    
    user_on_each_day = [0, 0, 0, 0, 0, 0, 0]
    user_on_weekdays = 0
    user_on_weekends = 0
    
    with open(filename, 'r') as f_in:
        Reader = csv.DictReader(f_in)
        
        for row in Reader:
            if row['user_type'] == usertype:
                if row['day_of_week'] == 'Monday':
                    user_on_each_day[0] += 1
                    user_on_weekdays += 1
                elif row['day_of_week'] == 'Tuesday':
                    user_on_each_day[1] += 1
                    user_on_weekdays += 1
                elif row['day_of_week'] == 'Wednesday':
                    user_on_each_day[2] += 1
                    user_on_weekdays += 1
                elif row['day_of_week'] == 'Thursday':
                    user_on_each_day[3] += 1
                    user_on_weekdays += 1
                elif row['day_of_week'] == 'Friday':
                    user_on_each_day[4] += 1
                    user_on_weekends += 1
                elif row['day_of_week'] == 'Saturday':
                    user_on_each_day[5] += 1
                    user_on_weekends += 1
                elif row['day_of_week'] == 'Sunday':
                    user_on_each_day[6] += 1
                    user_on_weekends += 1
    
    day_system_most_used = calendar.day_name[user_on_each_day.index(max(user_on_each_day))]
    
    x = np.arange(7)
    plt.bar(x, user_on_each_day, 0.5)
    plt.xticks(x, ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
    plt.title('Ridership on different days of the week for {}s in Washington.'.format(usertype))
    plt.xlabel('Day of week')
    plt.ylabel('Ridership')
    plt.show()
    
    if(user_on_weekdays > user_on_weekends):
        return "For {}: Ridership was greater on Weekdays as compared to Weekends. Maximum ridership was on {}".format(usertype, day_system_most_used)
    else:
        return "For {}: Ridership was greater on Weekends as compared to Weekdays. Maximum ridership was on {}".format(usertype, day_system_most_used)
             
data_file_Washington = './data/Washington-2016-Summary.csv'

print(per_day_analysis(data_file_Washington,'Subscriber'))
print(per_day_analysis(data_file_Washington,'Customer'))


In [1]:
from subprocess import call
call(['python', '-m', 'nbconvert', 'Bike_Share_Analysis.ipynb'])
Out[1]:
0
In [ ]:
