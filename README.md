# Streams Lib

A library to interact with [streamsapp.io](https://www.streamsapp.io/). This library provides functions to list streams, list entries, and add entries.

Primary purpose of this library is assist will creating scripts that import data into Streams from other services (e.g. importing nutritional data from myfitnesspal, or activity data from Fitbit).

## Installation

```
pip install git+https://github.com/streamsapp/streamslib
```

## Create a StreamsClient

`StreamsClient` is the object through which the Streams API is accessed. It provides methods: get_streams, get_entries, add_entry, and add_entries.

To create a client simply pass your email and password into the client:  

```
import streamslib

streams_client = StreamsClient('email', 'password')
```

It is advised to store your credentials as environment variables rather than in the code directly, see example.py for an example of this.

## Get Streams

The function `get_streams()` is provided to get streams.

```
streams = streamslib.get_stream()
```

The stream objects returned will have the following structure:

```
{
  "id": "...",
  "name": "workouts",
  "icon": "🏋️",
  "format": "...",
  "input_spec": { ... },
  "created": datetime.datetime(...),
  "modified": datetime.datetime(...)
}
```

## Get Entries

The function `get_entries(stream)` is provided to get entries as a pandas DataFrame.

```
streams = streamslib.get_stream()

stream = streams[0]

entries = streamslib.get_entries(stream)
```

## Add Entry

The function `add_entry(entry)` is provided to add entries to a stream.

```
contents = {
  'type': 'run',
  'distance': 1.8,
  'time': 12
}

entry = Entry(None, stream.id, contents, date)

streamslib.add_entry(entry)
```

## Add Entries

The function `add_entries(entries)` is provided to add multiple entries to a stream in bulk.

```
contents1 = { ... }
contents2 = { ... }

entries = [
  Entry(None, stream.id, contents1, date1),
  Entry(None, stream.id, contents2, date2),
  ...
]

streamslib.add_entries(entry)
```