import json

from bson import ObjectId

from .db import query_details


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

def _get_query(id):
    result = query_details.find_one({'_id': ObjectId(id)})
    if result:
        result['_id'] = str(result['_id'])
        metrics_result = _compute_ratios([result])[0]
        return metrics_result
    else:
        return {'ERROR': 'No matching data found.'}, 409

def _get_rsvp(result):
    accepted = [v for v in result['query']['responses'].values() if v['accepted'] == True]
    return len(accepted)
