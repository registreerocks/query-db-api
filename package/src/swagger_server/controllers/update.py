import datetime

from .create import _query_degree


def _add_infos(body, result):
    student_record = result.get('query').get('responses').get(body.get('student_address'))
    student_record['attended'] = True
    student_record['student_info'] = {
        'student_number': body.get('student_number'),
        'user_id': body.get('user_id')
    }
    return student_record

def _expand_add_responses(responses, query_results):
    for student_address, _ in query_results.items():
        if not responses.get(student_address):
            responses[student_address] = {
                'sent': '',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False
            }
    return responses

def _expand_query_degree(details, old_results):
    new_results = _query_degree(details)
    return {**old_results, **{student_address: value for student_address, value in new_results.items() if student_address not in old_results.keys()}}, new_results

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
    if 'accepted' in body:
        student_record['responded'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        student_record['accepted'] = body.get('accepted')
    return student_record

def _update_event_details(body, result):
    event = result.get('event')
    for key, value in body.items():
        if value: event[key] = value
    return event

def _add_attachments(body, result):
    return result.get('event').get('attachments') + body

def _delete_attachments(body, result):
    return [attachment for attachment in result.get('event').get('attachments') if attachment.get('id') not in body]
