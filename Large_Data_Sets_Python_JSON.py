#Working with large JSON datasets can be a pain, particularly when they are too
#large to fit into memory. In cases like this, a combination of command line
#tools and Python can make for an efficient way to explore and analyze the data.
#In this post, focused on learning python programming, we’ll look at how to
#leverage tools like Pandas to explore and map out police activity in
#Montgomery County, Maryland. We’ll start with a look at the JSON data,
#then segue into exploration and analysis of the JSON with Python.

#When data is stored in SQL databases, it tends to follow a rigid structure that
#looks like a table. Here’s an example from a SQLite database:

#id|code|name|area|area_land|area_water|population|population_growth|birth_rate|
#death_rate|migration_rate|created_at|updated_at1|af|Afghanistan|652230|652230|
#0|32564342|2.32|38.57|13.89|1.51|2015-11-01 13:19:49.461734|
#2015-11-01 13:19:49.4617342|al|Albania|28748|27398|1350|3029278|0.3|12.92|6.58|
#3.3|2015-11-01 13:19:54.431082|2015-11-01 13:19:54.4310823|ag|Algeria|2381741|
#2381741|0|39542166|1.84|23.67|4.31|0.92|2015-11-01 13:19:59.961286|
#2015-11-01 13:19:59.961286

#As you can see, the data consists of rows and columns, where each column maps
#to a defined property, like id, or code. In the dataset above, each row
#represents a country, and each column represents some fact about that country.

#But as the amount of data we capture increases, we often don’t know the exact
#structure of the data at the time we store it. This is called unstructured
#data. A good example is a list of events from visitors on a website.
#Here’s an example of a list of events sent to a server:

#{'event_type': 'started-mission', 'keen':
#{'created_at': '2015-06-12T23:09:03.966Z', 'id': '557b668fd2eaaa2e7c5e916b',
#'timestamp': '2015-06-12T23:09:07.971Z'}, 'sequence': 1}
#{'event_type': 'started-screen',
#'keen': {'created_at': '2015-06-12T23:09:03.979Z',
#'id': '557b668f90e4bd26c10b6ed6', 'timestamp': '2015-06-12T23:09:07.987Z'},
#'mission': 1, 'sequence': 4, 'type': 'code'} {'event_type': 'started-screen',
#'keen': {'created_at': '2015-06-12T23:09:22.517Z',
#'id': '557b66a246f9a7239038b1e0', 'timestamp': '2015-06-12T23:09:24.246Z'},
#'mission': 1, 'sequence': 3, 'type': 'code'},

#As you can see, three separate events are listed above. Each event has
#different fields, and some of the fields are nested within other fields.
#This type of data is very hard to store in a regular SQL database.
#This unstructured data is often stored in a format called
#JavaScript Object Notation (JSON). JSON is a way to encode data structures
#like lists and dictionaries to strings that ensures that they are easily
#readable by machines. Even though JSON starts with the word Javascript, it’s
#actually just a format, and can be read by any language.

#Python has great JSON support, with the json library. We can both convert
#lists and dictionaries to JSON, and convert strings to lists and dictionaries.
#JSON data looks much like a dictionary would in Python, with keys and values
#stored.

#In this post, we’ll explore a JSON file on the command line, then import it
#into Python and work with it using Pandas.

#The dataset

#We’ll be looking at a dataset that contains information on traffic violations in
#Montgomery County, Maryland.

#The data contains information about where the violation happened,
#the type of car, demographics on the person receiving the violation,
#and some other interesting information. There are quite a few questions
#we could answer using this dataset, including:


#What types of cars are most likely to be pulled over for speeding?
#What times of day are police most active?
#How common are “speed traps”? Or are tickets spread pretty evenly in terms of
#geography?
#What are the most common things people are pulled over for?


#Unfortunately, we don’t know the structure of the JSON file upfront,
#so we’ll need to do some exploration to figure it out.

#Extracting information on the columns

#Now that we know which key contains information on the columns, we need to
#read that information in. Because we’re assuming that the JSON file won’t fit
#in memory, we can’t just directly read it in using the json library.
#Instead, we’ll need to iteratively read it in in a memory-efficient way.

#We can accomplish this using the ijson package. ijson will iteratively parse
#the json file instead of reading it all in at once. This is slower than
#directly reading the whole file in, but it enables us to work with large
#files that can’t fit in memory. To use ijson, we specify a file we want to
#extract data from, then we specify a key path to extract:

import ijson
filename = "md_traffic.json"
with open(filename, 'r') as f:
    objects = ijson.items(f, 'meta.view.columns.item')
    columns = list(objects)

#In the above code, we open the md_traffic.json file, then we use the items
#method in ijson to extract a list from the file. We specify the path to the
#list using the meta.view.columns notation. Recall that meta is a top level key
#, which contains view inside, which contains columns inside it. We then
#specify meta.view.columns.item to indicate that we should extract each
#individual item in the in the meta.view.columns list. The items function
#wil return a generator, so we use the list method to turn the generator
#into a Python list. We can print out the first item in the list:

print(columns[0])

#From the above output, it looks like each item in columns is a dictionary that
#contains information about each column. In order to get our header, it looks
#like fieldName is the relevant key to extract. To get our column names, we just
#have to extract the fieldName key for each item in columns.

column_names = [col["fieldname"] for col in columns]column_names

#Great! Now that we have our columns names, we can move to extracting to data
#itself.

#Extracting the data

#You may recall that the data is locked away in a list of lists inside the
#data key. We'll need to read this data into memory to manipulate it.
#Fortunately, we can use the column names we just extracted to only grab the
#columns that are relevant. This will save a ton of space. If the dataset was
#larger, you could iteratively process batches of rows. So read in the first
#10000000 rows, do some processing, then the next 10000000, and so on. In this
#case, we can define the columns we care about, and again use ijson to
#iteratively process the JSON file:

good_columns = [
"date_of_stop",
"time_of_stop",
"agency",
"subagency",
"description",
"location",
"latitude",
"longitude",
"vehicle_type",
"year",
"make",
"model",
"color",
"violation_type",
"race",
"gender",
"driver_state",
"driver_city",
"dl_state",
"arrest_type"]
data = []
with open(filename, 'r') as f:
objects = ijson.items(f, 'data.item')
for row in objects:
    selected_row = []
for item in good_columns:
    selected_row.append(row[column_names.index(item)])
    data.append(selected_row)

#Now that we’ve read the data in, we can print out the first item in data:
print(data[0])


#Reading the data into Pandas
#Now that we have the data as a list of lists, and the column headers as a lits,
#we can create a Pandas Dataframe to analyze the data. If you're unfamiliar
#with Pandas, it's a data analysis library that uses an efficient, tabular
#data structure called a Dataframe to represent your data. Pandas allows you
#to convert a list of lists into a Dataframe and specify the column names
#separately

import pandas as pd
stops = pd.DataFrame(data, columns=good_columns)

#Now that we have our data in a Dataframe, we can do some interesting analysis
#Here's a table of how many stops are made by car color:

print(stops["color"].value_counts())

#Camouflage appears to be a very popular car color. Here's a table of what kind
#of police unit created the citation:

stops["arrest_type"].value_counts()

#With the rise of red light cameras and speed lasers, it's interesting that
#patrol cars are still by far the dominant source of citations.

#Converting columns

#We're now almost ready to do some time and location based analysis, but we
#need to convert the longitude, latitude, and date columns from strong to
#floats first. We can use the below code to convert latitude and longitude:

import numpy as np
def parse_float(x):
    try:
        x = floax(x)
    except Exception:
        x = 0
    return (xstops["longitude"] = stops["longitude"].apply(parse_float)
    stops["latitude"] = stops["latitude"].apply(parse_float))

#Oddly enough, time of day and the date of the stop are stored in two separate
#columns, time_of_stop, and date_of_stop. We'll parse both, and turn them into
#a single datetime column:

import datetime
def parse_full_date(row):
    date = datetime.datetime.strptime(row["date_of_stop"], "%Y-%m-%dT%H:%M:%S")
    time = row["time_of_stop"].split(":")
    date = date.replace(hour=int(time[0]), minute=int(time[1]), second =
    int(time[2]))
    return (datestops["date"] = stops.apply(parse_full_date, axis=1)

#We can now make a plot of which days result in the most traffic stops:
import matplotlib.pyplot as plt
%matplotlib inline plt.hist(stops["date"].dt.weekday, bins=6)
plt.show()

#In this plot, Monday is 0, and Sunday is 6. It looks like Sunday has the most
#stops, and Monday has the least. This could also be a data quality issue where
#invalid dates resulted in Sunday for some reason. You'll have to dig more
#deeply into the date_of_stop column to figure it out definitely.

#We can also plot out the most common traffic stop times:

plt.hist(stops["date"].dt.hour, bins=24)
plt.show()

#It looks like the most stops happen around midnight, and the fewest happen
#around 5am. This might make sense, as people are driving home from bars and
#dinners late at night, and may be impaired. This may also be a data quality
#issue, and poking through the time_of_stop column will be necessary to get the
#full answer.


#Subsetting the stops
#Now that we've converted the location and date columns, we can map out the
#traffic stops. Because mapping is very intensive in terms of CPU resources and
#memory, we'll need to filter down the rows we use from stops first:

last_year = stops[stops["date"] > datetime.datetime(year=2018, month=7, day=25)]

#In the above code, we selected all of the rows that came in the past year. We
#can further narrow this down, and select rows that occured during rush hour --
#the morning period when everyone is going to work:

morning_runs = last_year[(last_year["date"].dt.weekday < 5) &
(last_year["date"].dt.hour > 5) & (last_year["date"].dt.hour < 10)]

#Using the excellent folium package, we can now visualize where all the stops
#occured. Folium allows ou to easily create interactive maps in Python by
#leveraging leaflet. In order to perserve performance, we'll only visualize
#the first 1000 rows of morning_rush:

import folium
from folium import plugins
stops_map = folium.Map(location=[39.0836, -77.1483], zoom_start=11)
marker_cluster = folium.MarkerCluster().add_to(stops_map)
for name, row in morning_rush.iloc[:1000].iterrows():
    folium.Marker([row["longitude"], row["latitude"]], popup=row["description"])
    .add_to(marker_cluster)
    stops_map.create_map('stops.html')stops_map

#This shows that many traffic stops are concentrated around the bottom right
#of the country. We can extend our analysis further with a heatmap:

stops_heatmap = folium.Map(location=[39.0836, -77.1483],
zoom_start=11)stops_heatmap.add_children(plugins.HeatMap([[row["longitude"],
row["latitude"]]
for name, row in morning_rush.iloc[:1000].iterrows()]))
stops_heatmap.save("heatmap.html")stops_heatmap