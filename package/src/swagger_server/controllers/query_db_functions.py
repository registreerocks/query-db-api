import datetime
import json
from os import environ as env

import requests
from bson import ObjectId
from pymongo import MongoClient

from .authentication import (get_token_auth_header, requires_auth,
                             requires_scope)
from .helpers import check_id

BIGCHAINDB_URL = env.get('BIGCHAINDB_URL')

client = MongoClient('mongodb://mongodb:27017/')
db = client.query_database
query_details = db.query_details

@requires_auth
@requires_scope('registree', 'recruiter')
def post_query(body):
    token = get_token_auth_header()
    query = body.get('query')
    details = query.get('details')
    query_results = []
    for item in details:
        query = {
            'university_id': item.get('university_id'),
            'degree_id': item.get('degree_id'),
            'course_id': item.get('course_id')
        }
        if item.get('course_id'):
            query['result'] = _query('course', item.get('course_id'), item, token)
        elif item.get('degree_id'):
            query['result'] = _query('degree', item.get('degree_id'), item, token)
        else:
            query['result'] = {}
        query_results.append(query)
    query['results'] = query_results
    query['responses'] = _notify_students(query_results)
    query['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    body['query'] = query
    return str(query_details.insert_one(body).inserted_id)

@requires_auth
@requires_scope('registree', 'recruiter')
@check_id
def get_query(id):
    result = query_details.find_one({'_id': ObjectId(id)})
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree', 'recruiter')
def get_queries_by_customer(customer_id):
    result = query_details.find({'customer_id': customer_id})
    if result:
        return _stringify_object_id(result)
    else:
        return {'ERROR': 'No matching data found.'}, 409

def _query(_type, _id, item, token):
    headers = {'Authorization': 'Bearer ' + token}
    if item.get('absolute'):
        payload = {_type + '_id': _id, 'x': item.get('absolute')}
        response = requests.get(BIGCHAINDB_URL + '/query/' + _type + '/top_x', params=payload, headers=headers)
        return json.loads(response.text)
    elif item.get('percentage'):
        payload = {_type + '_id': _id, 'x': item.get('percentage')}
        response = requests.get(BIGCHAINDB_URL + '/query/' + _type + '/top_x_percent', params=payload, headers=headers)
        return json.loads(response.text)
    else:
        return {"ERROR": "No filter given."}, 400

def _notify_students(query_results):
    notifications = {}
    for _, results in query_results.items():
        for student_id, _ in results.items():
            notifications[student_id] = 'sent'
    return notifications

def _stringify_object_id(result):
    stringified_result = []
    for element in result:
        element['_id'] = str(element['_id'])
        stringified_result.append(element)
    return stringified_result