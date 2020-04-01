import datetime
import json
from os import environ as env

import requests

STUDENT_DB_URL = env.get('STUDENT_DB_URL', 'http://example.com')

def _add_responses(query_results):
    responses = {}
    for result in query_results:
        responses[result['student_address']] = {
            'sent': '',
            'viewed': '',
            'responded': '',
            'accepted': False,
            'attended': False
        }
    return responses

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

def _query(details, token):
    query_list = _build_query(details)
    query_results = []
    try:
        query_response = _query_student_db(query_list, token)
        for i in range(len(query_list)):
            query_results += query_response.get(str(i))
        return query_results
    except ValueError: raise

def _query_student_db(query_list, token):
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    body = {'query_list': query_list}
    response = requests.post(STUDENT_DB_URL + '/query/bulk', data=json.dumps(body), headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise ValueError('Query not possible, status code: '+ str(response.status_code))

