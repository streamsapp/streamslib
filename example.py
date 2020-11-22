import os
from streamslib import StreamsClient, Entry
import myfitnesspal
import datetime as dt

# login
streams_client = StreamsClient(os.environ['STREAMS_USER'], os.environ['STREAMS_PASSWORD'])

# get nutrition stream
streams = streams_client.get_streams()

try:
  nutrition_stream = next(stream for stream in streams if stream.name == 'Nutrition')
except:
  print('Could not find stream')
  exit()

# get latest entry date
entries = streams_client.get_entries(nutrition_stream)

# default to 2 weeks ago if no entries found
latest_entry_date = (entries['date'].max() + dt.timedelta(days=1) if len(entries) > 0 
                      else dt.datetime.today() - dt.timedelta(days=14)).date()

# read from myfitnesspal
client = myfitnesspal.Client(os.environ['MYFITNESSPAL_USER'], os.environ['MYFITNESSPAL_PASSWORD'])

no_of_days_to_import = dt.datetime.today().date() - latest_entry_date

print('Importing %s day(s)' % (no_of_days_to_import.days))

entries_to_add = []

for i in range(0, no_of_days_to_import.days):
  date = latest_entry_date + dt.timedelta(days=i)
  nutrition = client.get_date(date.year, date.month, date.day)
  
  print(date)

  if 'calories' not in nutrition.totals:
    continue

  contents = {
    'calories': nutrition.totals['calories'],
    'carbs': nutrition.totals['carbohydrates'],
    'fat': nutrition.totals['fat'],
    'protein': nutrition.totals['protein'],
    'sugar': nutrition.totals['sugar']
  }

  print(contents)

  entry = Entry(None, nutrition_stream.id, contents, date)
  entries_to_add.append(entry)

if len(entries_to_add) > 0:
  streams_client.add_entries(entries_to_add)

print('✔')