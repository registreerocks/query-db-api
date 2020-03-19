import datetime
import json
from os import environ as env

import requests
from bson import ObjectId
from pymongo import MongoClient

from .authentication import (get_token_auth_header, requires_auth,
                             requires_scope)
from .helpers import check_id

STUDENT_DB_URL = env.get('STUDENT_DB_URL', 'http://example.com')

CLIENT = MongoClient('mongodb://mongodb:27017/')
DB = CLIENT.database
query_details = DB.query_db

@requires_auth
@requires_scope('recruiter')
def post_query(body):
    token = get_token_auth_header()
    query = body.get('query')
    try:
        query['results'] = _query(query.get('details'), token)
        query['responses'] = _notify_students(query['results'])
        query['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        body['query'] = query
        return str(query_details.insert_one(body).inserted_id)
    except ValueError as e:
        return {'ERROR': str(e)}, 500

@requires_auth
@requires_scope('recruiter')
@check_id
def get_query(id):
    return _get_query(id)

@requires_auth
@requires_scope('recruiter', 'registree')
def get_queries_by_customer(customer_id):
    result = query_details.find({'customer_id': customer_id})
    if result:
        metrics_result = _compute_ratios(result)
        return _stringify_object_id(metrics_result)
    else:
        return {'ERROR': 'No matching data found.'}, 409

@check_id
@requires_auth
@requires_scope('recruiter', 'student')
def update_status(id, body):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        student_record = _set_status(body, result)
        query_details.update_one({'_id': ObjectId(id)}, {'$set': {'query.responses.' + body.get('student_address'): student_record}}, upsert=False)
        return id

@requires_auth
@requires_scope('recruiter', 'student')
@check_id
def update(id, body):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        event = _update_event_details(body, result)
        query_details.update_one({'_id': ObjectId(id)}, {'$set': {'event': event}}, upsert=False)
        return _get_query(id)

@requires_auth
@requires_scope('recruiter')
@check_id
def expand_query(id, body):
    token = get_token_auth_header()
    query = query_details.find_one({'_id': ObjectId(id)})
    if not query:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        try:
            expanded_result, new_result = _expand_query(body, query.results, token)
            expanded_notifications = _expand_notify_students(query.responses, new_result)
            query_details.update_one(
                {'_id': ObjectId(id)}, 
                {'$set': {
                    'query.details': body,
                    'query.results': expanded_result, 
                    'query.responses': expanded_notifications, 
                    'query.timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
                    }
                }, upsert=False)
            return _get_query(id)
        except ValueError as e:
            return {'ERROR': str(e)}, 500

@check_id
@requires_auth
@requires_scope('recruiter', 'student')
def add_student_attendance(id, body):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        student_record = _add_infos(body, result)
        query_details.update_one({'_id': ObjectId(id)}, {'$set': {'query.responses.' + body.get('student_address'): student_record}}, upsert=False)
        return id

@requires_auth
@requires_scope('student')
def get_queries_by_student(student_address):
    results = query_details.find({'query.results.student_address': student_address})
    return _build_student_result(student_address, results)

def _get_query(id):
    result = query_details.find_one({'_id': ObjectId(id)})
    if result:
        result['_id'] = str(result['_id'])
        metrics_result = _compute_ratios([result])[0]
        return metrics_result
    else:
        return {'ERROR': 'No matching data found.'}, 409

def _query(details, token):
    query_list = _build_query(details)
    query_results = []
    try:
        query_response = _query_student_db(query_list, token)
        for i in range(len(query_list)):
            query_results += query_response.get(str(i))
        return query_results
    except ValueError: raise

def _expand_query(details, old_results, token):
    try:
        new_results = _query(details, token)
        for item in new_results:
            if item not in old_results:
                old_results.append(item)
        return old_results
    except ValueError: raise

def _build_query(details):
    query_list = []
    for item in details:
        if item.get('course_id'):
            query_list.append({
                'type': 'course',
                'type_id': item.get('course_id'),
                'x': item.get('absolute', 0) | item.get('percentage', 0),
                'absolute': True if item.get('absolute', 0) > item.get('percentage', 0) else False
            })
        elif item.get('degree_id'):
            query_list.append({
                'type': 'degree',
                'type_id': item.get('degree_id'),
                'x': item.get('absolute', 0) | item.get('percentage', 0),
                'absolute': True if item.get('absolute', 0) > item.get('percentage', 0) else False
            })
        elif item.get('faculty_id'):
            query_list.append({
                'type': 'faculty',
                'type_id': item.get('faculty_id'),
                'x': item.get('absolute', 0) | item.get('percentage', 0),
                'absolute': True if item.get('absolute', 0) > item.get('percentage', 0) else False
            })
    return query_list

def _query_student_db(query_list, token):
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    body = {'query_list': query_list}
    response = requests.post(STUDENT_DB_URL + '/query/bulk', data=json.dumps(body), headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise ValueError('Query not possible, status code: '+ str(response.status_code))

def _notify_students(query_results):
    notifications = {}
    for result in query_results:
        notifications[result['student_address']] = {
            'sent': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
            'viewed': '',
            'responded': '',
            'accepted': False,
            'attended': False
        }
    return notifications

def _expand_notify_students(notifications, query_results):
    for result in query_results:
        if not notifications.get(result['student_address']):
            notifications[result['student_address']] = {
                'sent': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False
            }
    return notifications

def _compute_ratios(results):
    updated_results = []
    for result in results:
        responses = result.get('query').get('responses')
        viewed = responded = accepted = attended = 0
        for _, value in responses.items():
            if value['viewed']:
                viewed += 1
            if value['responded']:
                responded += 1
            if value['accepted']:
                accepted += 1
            if value['attended']:
                attended += 1
        result['query']['metrics'] = {
            'viewed': viewed, 
            'responded': responded, 
            'accepted': accepted, 
            'attended': attended
            }
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

def _add_infos(body, result):
    student_record = result.get('query').get('responses').get(body.get('student_address'))
    student_record['attended'] = True
    student_record['student_info'] = {
        'student_id': body.get('student_id'),
        'first_name': body.get('first_name'),
        'last_name': body.get('last_name')
    }
    return student_record

def _update_event_details(body, result):
    event = result.get('event')
    for key, value in body.items():
        event[key] = value
    return event

def _build_student_result(student_address, results):
    student_results = []
    for result in results:
        student_result = {
            '_id': str(result.get('_id')),
            'customer_id': result.get('customer_id'),
            'event': result.get('event'),
            'response': result.get('query').get('responses').get(student_address),
            'timestamp': result.get('query').get('timestamp'),
            'qr': json.dumps({'query_id': str(result.get('_id')), 'student_address': student_address})
        }
        student_results.append(student_result)
    return student_results

def _stringify_object_id(result):
    stringified_result = []
    for element in result:
        element['_id'] = str(element['_id'])
        stringified_result.append(element)
    return stringified_result
