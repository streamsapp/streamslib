import unittest
from streamslib import Stream, Entry
import datetime as dt

# TODO: It would be nice to actually test the main class i.e. StreamsClient. We could do by spinning up 
#       streams-server using test containers and pointing StreamsClient at that.

class StreamLibTests(unittest.TestCase):

  def test_create_stream(self):
    stream = Stream.from_json({
      'id': 'blah',
      'name': 'Streamy',
      'format': '',
      'inputSpec': {'fields': []}, 
      'createdDate': '2020-06-01T12:34:56+01:00',
      'modifiedDate': '2020-06-02T23:12:55+01:00'
    })
    
    self.assertEqual(stream.id, 'blah')
    self.assertEqual(stream.name, 'Streamy')
    self.assertEqual(stream.created_date, dt.datetime(2020, 6, 1, 12, 34, 56, tzinfo=dt.timezone(dt.timedelta(hours=1))))
    self.assertEqual(stream.modified_date, dt.datetime(2020, 6, 2, 23, 12, 55, tzinfo=dt.timezone(dt.timedelta(hours=1))))


  def test_create_entry(self):
    entry = Entry.from_json({
      'id': 'blarn',
      'streamId': 'blah',
      'contents': { 'field': 'value' },
      'date': '2020-06-01T12:34:56+05:00',
      'createdDate': '2020-06-01T12:34:56+01:00',
      'modifiedDate': '2020-06-02T23:12:55+01:00'
    })
    
    self.assertEqual(entry.id, 'blarn')
    self.assertIsNotNone(entry.stream_id, 'blah')
    self.assertEqual(entry.contents, { 'field': 'value' })
    self.assertEqual(entry.date, dt.datetime(2020, 6, 1, 12, 34, 56, tzinfo=dt.timezone(dt.timedelta(hours=5))))
    self.assertIsNotNone(entry.created_date)
    self.assertIsNotNone(entry.modified_date)


if __name__ == '__main__':
    unittest.main()
