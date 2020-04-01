import datetime

from .create import _query


def _add_infos(body, result):
    student_record = result.get('query').get('responses').get(body.get('student_address'))
    student_record['attended'] = True
    student_record['student_info'] = {
        'student_id': body.get('student_id'),
        'first_name': body.get('first_name'),
        'last_name': body.get('last_name')
    }
    return student_record

def _expand_add_responses(responses, query_results):
    for result in query_results:
        if not responses.get(result['student_address']):
            responses[result['student_address']] = {
                'sent': '',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False
            }
    return responses

def _expand_query(details, old_results, token):
    try:
        new_results = _query(details, token)
        for item in new_results:
            if item not in old_results:
                old_results.append(item)
        return old_results
    except ValueError: raise

def _notify_students(responses):
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    students = []
    for k, v in responses.items():
        if not v['sent']:
            v['sent'] = timestamp
            students.append(k)
    return responses, students

def _set_status(body, result):
    student_record = result.get('query').get('responses').get(body.get('student_address'))
    if 'viewed' in body:
        student_record['viewed'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    elif 'accepted' in body:
        student_record['responded'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        student_record['accepted'] = body.get('accepted')
    return student_record

def _update_event_details(body, result):
    event = result.get('event')
    for key, value in body.items():
        event[key] = value
    return event
