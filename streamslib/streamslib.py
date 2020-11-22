from __future__ import annotations

import requests
import datetime as dt
import pandas as pd
from typing import List
import uuid
import urllib.parse
import dateutil.parser

class Token:
  access_token: str
  refresh_token: str

  def __init__(self, access_token: str, refresh_token: str):
    self.access_token = access_token
    self.refresh_token = refresh_token

  @staticmethod
  def from_json(json: dict) -> Token:
    return Token(json['accessToken'], json['refreshToken'])


class Field:
  id: str
  name: str
  type: str
  values: List[str]

  def __init__(self, id: str, name: str, type: str, values: List[str]):
    self.id = id
    self.name = name
    self.type = type
    self.values = values

  @staticmethod
  def from_json(json: dict) -> Field:
    return Field(json['id'], json['name'], json['type'], json['values'])


class InputSpec:
  fields: List[Field]

  def __init__(self, fields: List[Field]):
    self.fields = fields


  @staticmethod
  def from_json(json: List[dict]) -> InputSpec:
    return InputSpec(list(map(lambda f: Field.from_json(f), json['fields'])))


class Stream:
  id: str
  name: str
  format: str
  input_spec: InputSpec
  created_date: dt.datetime
  modified_date: dt.datetime

  def __init__(self, id: str, name: str, format: str, input_spec: InputSpec, created_date: dt.datetime, modified_date: dt.datetime):
    self.id = str(uuid.uuid4()) if id is None else id
    self.name = name
    self.format = format
    self.input_spec = input_spec
    self.created_date = created_date
    self.modified_date = modified_date

  @staticmethod
  def from_json(json: dict) -> Stream:
    return Stream(json['id'], json['name'], json['format'], InputSpec.from_json(json['inputSpec']), 
          dateutil.parser.isoparse(json['createdDate']),
          dateutil.parser.isoparse(json['modifiedDate']))


class Entry:
  id: str
  stream_id: str
  contents: dict
  date: dt.datetime
  created_date: dt.datetime
  modified_date: dt.datetime

  def __init__(self, id: str, stream_id: str, contents: dict, date: dt.datetime,
                created_date: dt.datetime = dt.datetime.now().replace(microsecond=0),
                modified_date: dt.datetime = dt.datetime.now().replace(microsecond=0)):
    self.id = str(uuid.uuid4()) if id is None else id
    self.stream_id = stream_id
    self.contents = contents
    self.date = date if isinstance(date, dt.datetime) else dt.datetime.combine(date, dt.time(12, 0, 0, 0)) 
    self.created_date = created_date
    self.modified_date = modified_date

  @staticmethod
  def from_json(json: dict) -> Entry:
    return Entry(json['id'], json['streamId'], json['contents'],
          dateutil.parser.isoparse(json['date']),
          dateutil.parser.isoparse(json['createdDate']),
          dateutil.parser.isoparse(json['modifiedDate']))

  def to_json(self) -> dict:
    return {
      'id': self.id,
      'streamId': self.stream_id,
      'contents': self.contents,
      'date': self.date.astimezone().isoformat(),
      'createdDate': self.created_date.astimezone().isoformat(),
      'modifiedDate': self.modified_date.astimezone().isoformat()
    }


class StreamsClient:
  __api_url: str
  __token: Token

  def __init__(self, email: str, password: str, api_url='https://api.streamsapp.io') -> Token:
    self.__api_url = api_url
    
    headers = { 'Content-Type': 'application/json' }
    response = requests.post(self.__api_url + '/login', headers=headers, json={ "username": email, "password": password })
    
    if response.status_code == 401 or response.status_code == 403:
      raise Exception('Invalid credentials: ' + response.text)

    if response.status_code != 200:
      raise Exception('Could not log in: ' + response.text)
    
    self.__token = Token.from_json(response.json())


  def get_streams(self) -> List[Stream]:
    headers = { "Authorization": "Bearer " + self.__token.access_token}

    response = requests.get(self.__api_url + '/streams', headers=headers)

    if response.status_code == 401:
      raise Exception('Unauthorized - invalid token')

    if response.status_code != 200:
      raise Exception('Could not retrieve streams: ' + response.text)

    streams = response.json()

    result = []

    for stream in streams:
      result.append(Stream.from_json(stream))

    return result

  def get_entries(self, stream: Stream) -> pd.DataFrame:
    headers = { "Authorization": "Bearer " + self.__token.access_token }
    response = requests.get(self.__api_url + '/streams/' + stream.id + '/entries', headers=headers)

    if response.status_code == 401:
      raise Exception('Unauthorized - invalid token')

    if response.status_code == 404:
      raise Exception('Could not find stream with id=' + stream.id)

    if response.status_code != 200:
      raise Exception('Could not retrieve entries')

    entries = response.json()
    normalised_entries = []

    name_map = { f.id: f.name for f in stream.input_spec.fields }

    for entry in entries:

      contents = {}

      for (k, v) in entry['contents'].items():
        if k in name_map:
          contents[name_map[k]] = v

      normalised_entries.append(dict(id=entry['id'], streamId=entry['streamId'], date=dateutil.parser.isoparse(entry['date']), **contents ))

    return pd.DataFrame.from_dict(normalised_entries)


  def add_entry(self, entry: Entry) -> None:
    headers = { "Authorization": "Bearer " + self.__token.access_token }

    response = requests.post(self.__api_url + '/streams/' + entry.stream_id + '/entries', headers=headers, json=entry.to_json())

    if response.status_code == 401:
      raise Exception('Unauthorized - invalid token')

    if response.status_code == 404:
      raise Exception('Could not find stream with id=' + entry.stream_id)

    if response.status_code != 200:
      print(response.text)
      raise Exception('Could not add entry: ' + str(response.status_code))


  def add_entries(self, entries: List[Entry]):
    headers = { 'Authorization': 'Bearer ' + self.__token.access_token}
    
    body = {
      'modifiedStreams': [],
      'deletedStreams': [],
      'modifiedEntries': list(map(lambda e: e.to_json(), entries)),
      'deletedEntries': []
    }

    response = requests.post(self.__api_url + '/sync?date=' + urllib.parse.quote(dt.datetime.now().replace(microsecond=0).astimezone().isoformat()), headers=headers, json=body)

    if response.status_code == 401:
      raise Exception('Unauthorized - invalid token')

    if response.status_code != 200:
      print(response.text)
      raise Exception('Could not add entries: ' + str(response.status_code))