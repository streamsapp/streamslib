# Streams Lib

A library to interact with [streamsapp.io](https://www.streamsapp.io/). This library provides functions to list streams, list entries, and add entries.

Primary purpose of this library is assist will creating scripts that import data into Streams from other services (e.g. importing nutritional data from myfitnesspal, or activity data from Fitbit).

## Installation

```
pip install git+https://github.com/streamsapp/streamslib
```

## Authorisation Token

Streams uses tokens to provide access to streams and entries. A long lived token can be created in the [account section](https://www.streamsapp.io/#/account) of the app. In the examples below we have created an environment variable called `STREAMS_ACCESS_TOKEN` which stores an access token.

## Get Streams

The functions `get_streams(token)` and `get_stream(token, stream_name)` are provided to get streams.

```
import streamslib
import os

token = os.environ['STREAMS_ACCESS_TOKEN']

all_streams = streamslib.get_streams(token)

# or

nutrition = streamslib.get_stream(token, 'nutrition')
```

The stream objects returned will have the following structure:

```
{
  "streamId": "...",
  "name": "workouts",
  "icon": "🏋️",
  "created": datetime.datetime(...),
  "modified": datetime.datetime(...)
}
```

## Get Entries

The function `get_entries(token, stream_id)` is provided to get entries.

```
import streamslib
import os

token = os.environ['STREAMS_ACCESS_TOKEN']
nutrition = streamslib.get_stream(token, 'nutrition')
entries = streamslib.get_entries(token, nutrition['streamId'])
```

The entries objects returned will have the following structure:

```
[
  {
    "entryId": "...",
    "streamId": "..."
    "body": "calories: 1596",
    "date": datetime.datetime(...),
    "modified": datetime.datetime(...)
  },
  ...
]
```

## Add Entry

The function `add_entry(token, stream_id, entry)` is provided to add entries to a stream.


```
import streamslib
import os
import datetime as dt

token = os.environ['STREAMS_ACCESS_TOKEN']
nutrition = streamslib.get_stream(token, 'nutrition')

entry = {
  'text': 'Hello from Python',
  'date': dt.datetime.today()
}

entry = streamslib.add_entries(token, nutrition['streamId'], entry)
```

The entry object returned will have the following structure:

```
{
  "entryId": "...",
  "streamId": "...",
  "body": "calories: 1596",
  "date": datetime.datetime(...),
  "modified": datetime.datetime(...)
}
```

