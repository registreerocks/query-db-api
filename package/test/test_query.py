import mock
import pytest
import pymongo
from bson.objectid import ObjectId
import random

from src.swagger_server.controllers.query import _get_top_x, _get_top_x_percent, _query_bulk


@mock.patch('pymongo.collection.Collection.find')
def test_get_top_x(mock_mongo_find):
  random.seed(0)
  mock_mongo_find.return_value = get_course_average_blob()
  assert(len(_get_top_x(10, 'course', '5d7a4090b61d9af587ffa1b4')) == 10)
  assert(len(_get_top_x(20, 'course', '5d7a4090b61d9af587ffa1b4')) == 20)
  assert(len(_get_top_x(25, 'course', '5d7a4090b61d9af587ffa1b4')) == 20)
  output = _get_top_x(10, 'course', '5d7a4090b61d9af587ffa1b4')
  assert(len(list(set(list(output.keys())))) == 10)
  assert(_get_top_x(2, 'course', '5d7a4090b61d9af587ffa1b4') == _get_query_result())


@mock.patch('pymongo.collection.Collection.find')
def test_get_top_x_percent(mock_mongo_find):
  random.seed(0)
  mock_mongo_find.return_value = get_course_average_blob()
  assert(len(_get_top_x_percent(10, 'course', '5d7a4090b61d9af587ffa1b4')) == 2)
  assert(len(_get_top_x_percent(50, 'course', '5d7a4090b61d9af587ffa1b4')) == 10)
  assert(len(_get_top_x_percent(100, 'course', '5d7a4090b61d9af587ffa1b4')) == 20)
  output = _get_top_x_percent(50, 'course', '5d7a4090b61d9af587ffa1b4')
  assert(len(list(set(list(output.keys())))) == 10)
  assert(_get_top_x_percent(10, 'course', '5d7a4090b61d9af587ffa1b4') == _get_query_result())

@mock.patch('pymongo.collection.Collection.find')
def test_bulk_query(mock_mongo_find):
  random.seed(0)
  mock_mongo_find.return_value = get_course_average_blob()
  query_list = [{
    'type': 'course',
    'type_id': '5d7a4090b61d9af587ffa1b4',
    'x': 2,
    'absolute': True
    },
    {
    'type': 'course',
    'type_id': '5d7a4090b61d9af587ffa1b5',
    'x': 1,
    'absolute': False
    }]
  result =_query_bulk(query_list)
  assert(len(result.keys()) == 2)
  assert(len(result['5d7a4090b61d9af587ffa1b4']) == 2)
  assert(len(result['5d7a4090b61d9af587ffa1b5']) == 1)
  assert(result == _get_bulk_query_result())
    

def get_course_average_blob():
  fake_data = []
  for course_id in ['5d7a4090b61d9af587ffa1b4', '5d7a4090b61d9af587ffa1b5']:
    for address in ['0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07', '0x08', '0x09', '0x10', '0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x17', '0x18', '0x19']:
      for term in [2016, 2017, 2018, 2019]:
        bodyAverage = {
          'asset': {
            'data': {
              'asset_type': 'course_average',
              'course_id': course_id,
              'degree_id': '5d7a4090b61d9af587ffa1b6',
              'faculty_id': '5d7a4090b61d9af587ffa1b7',
              'semester': 1,
              'student_address': address,
              'term': term,
              'university_id': '5d7a4090b61d9af587ffa1b8'
            }
          },
          'metadata': {
            'avg': random.randint(0, 100),
            'complete': True
          }
        }
        fake_data.append(bodyAverage)
  return fake_data

def _get_query_result():
  return {
    '0x09': {'avg': 90, 'complete': True, 'term': 2019},
    '0x16': {'avg': 93, 'complete': True, 'term': 2019}
  }

def _get_bulk_query_result():
  return {
    '5d7a4090b61d9af587ffa1b4': _get_query_result(),
    '5d7a4090b61d9af587ffa1b5': {'0x16': {'avg': 93, 'complete': True, 'term': 2019}}
  }