import json

from bson import ObjectId

from .db import query_details

def _build_customer_result(results):
    customer_results = []
    for result in results:
        result['query']['metrics'] = _compute_ratios(result.get('query').get('responses'))
        customer_results.append(result)
    return customer_results

def _build_registree_result(results):
    registree_results = []
    for result in results:
        result['query']['metrics'] = _compute_ratios(result.get('query').get('responses'))
        result['query'].pop('results')
        # result['query'].pop('responses')
        registree_results.append(result)
    return registree_results


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

def _compute_ratios(responses):
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
    return {
        'viewed': viewed, 
        'responded': responded, 
        'accepted': accepted, 
        'attended': attended
        }

def _get_query(id):
    result = query_details.find_one({'_id': ObjectId(id)})
    if result:
        result['_id'] = str(result['_id'])
        result['query']['metrics'] = _compute_ratios(result.get('query').get('responses'))
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

def _get_rsvp(result):
    accepted = [v for v in result['query']['responses'].values() if v['accepted'] == True]
    return len(accepted)
