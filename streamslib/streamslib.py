import requests
import datetime as dt

API_URL = 'https://api.streamsapp.io'

def get_streams(token):
  headers = { "Authorization": "Bearer " + token}

  response = requests.get(API_URL + '/streams', headers=headers)

  if response.status_code == 401:
    raise Exception('Unauthorized - invalid token')

  if response.status_code != 200:
    raise Exception('Could not retrieve streams')

  streams = response.json()['streams']

  return streams

def get_stream(token, stream_name):
  streams = get_streams(token)
  stream = [stream for stream in streams if stream['name'] == stream_name]

  if len(stream) == 0:
    raise Exception('Could not find stream with name=' + stream_name)

  return stream[0]

def get_entries(token, stream_id):
  headers = { "Authorization": "Bearer " + token}
  response = requests.get(API_URL + '/stream/' + stream_id, headers=headers)

  if response.status_code == 401:
    raise Exception('Unauthorized - invalid token')

  if response.status_code == 404:
    raise Exception('Could not find stream with id=' + stream_id)

  if response.status_code != 200:
    raise Exception('Could not retrieve entries')

  entries = response.json()['entries']

  for entry in entries:
    entry['date'] = dt.datetime.strptime(entry['date'], '%Y-%m-%dT%H:%M:%S')

  return entries

def add_entry(token, stream_id, entry):
  headers = { "Authorization": "Bearer " + token}
  response = requests.post(API_URL + '/stream/' + stream_id, headers=headers, json=entry)

  if response.status_code == 401:
    raise Exception('Unauthorized - invalid token')

  if response.status_code == 404:
    raise Exception('Could not find stream with id=' + stream_id)

  if response.status_code != 200:
    raise Exception('Could not add entry')

  entry = response.json()
  entry['date'] = dt.datetime.strptime(entry['date'], '%Y-%m-%dT%H:%M:%S')

  return entry
