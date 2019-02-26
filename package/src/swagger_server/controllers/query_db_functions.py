import datetime
import json
from os import environ as env

import requests
from bson import ObjectId
from pymongo import MongoClient

from .authentication import (get_token_auth_header, requires_auth,
                             requires_scope)
from .helpers import check_id

BIGCHAINDB_URL = env.get('BIGCHAINDB_URL', 'http://example.com')

client = MongoClient('mongodb://mongodb:27017/')
db = client.query_database
query_details = db.query_details

@requires_auth
@requires_scope('registree', 'recruiter')
def post_query(body):
    token = get_token_auth_header()
    query = body.get('query')
    query['results'] = _query(query.get('details'), token)
    query['responses'] = _notify_students(query['results'])
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
        metrics_result = _compute_ratios([result])[0]
        return metrics_result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree', 'recruiter')
def get_queries_by_customer(customer_id):
    result = query_details.find({'customer_id': customer_id})
    if result:
        metrics_result = _compute_ratios(result)
        return _stringify_object_id(metrics_result)
    else:
        return {'ERROR': 'No matching data found.'}, 409

def update_status(body):
    result = query_details.find_one({'_id': ObjectId(body.get('id'))})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        student_record = _set_status(body, result)
        return query_details.update_one({'_id': ObjectId(body.get('id'))}, {'$set': {'query.responses.' + body.get('student_address'): student_record}}, upsert=False)

def _query(details, token):
    query_results = []
    for item in details:
        query_result = {
            'university_id': item.get('university_id'),
            'degree_id': item.get('degree_id'),
            'course_id': item.get('course_id')
        }
        try:
            if item.get('course_id'):
                query_result['result'] = _query_bigchaindb('course', item.get('course_id'), item, token)
            elif item.get('degree_id'):
                query_result['result'] = _query_bigchaindb('degree', item.get('degree_id'), item, token)
            else:
                query_result['result'] = {}
        except ValueError as exp:
            return {"ERROR": exp}
        query_results.append(query_result)
    return query_results

def _query_bigchaindb(_type, _id, item, token):
    headers = {'Authorization': 'Bearer ' + token}
    if item.get('absolute'):
        payload = {_type + '_id': _id, 'x': item.get('absolute')}
        response = requests.get(BIGCHAINDB_URL + '/query/' + _type + '/top_x', params=payload, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise ValueError('Query not possible')
    elif item.get('percentage'):
        payload = {_type + '_id': _id, 'x': item.get('percentage')}
        response = requests.get(BIGCHAINDB_URL + '/query/' + _type + '/top_x_percent', params=payload, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise ValueError('Query not possible')
    else:
        raise ValueError('No filter given.')

def _notify_students(query_results):
    notifications = {}
    for result in query_results:
        for student in result['result']:
            notifications[student['student_address']] = {
                'sent': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
                'viewed': '',
                'responded': '',
                'accepted': False
            }
    return notifications

def _compute_ratios(results):
    updated_results = []
    for result in results:
        responses = result.get('query').get('responses')
        viewed = responded = accepted = 0
        for _, value in responses.items():
            if value['viewed']:
                viewed += 1
            if value['responded']:
                responded += 1
            if value['accepted']:
                accepted += 1
        result['query']['metrics'] = {'viewed': viewed / len(responses), 'responded': responded / len(responses), 'accepted': accepted / len(responses)}
        updated_results.append(result)
    return updated_results

def _set_status(body, result):
    student_record = result.get('query').get('responses').get(body.get('student_address'))
    if 'viewed' in body:
        student_record['viewed'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    elif 'accepted' in body:
        student_record['responded'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        student_record['accepted'] = body.get('accepted')
    return student_record

def _stringify_object_id(result):
    stringified_result = []
    for element in result:
        element['_id'] = str(element['_id'])
        stringified_result.append(element)
    return stringified_result