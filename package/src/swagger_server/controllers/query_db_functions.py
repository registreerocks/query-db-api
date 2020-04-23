import datetime

from bson import ObjectId

from registree_auth import get_token_auth_header, requires_auth, requires_scope

from .create import _add_responses, _query_degree
from .db import query_details
from .get import _build_student_result, _compute_ratios, _get_query, _get_rsvp
from .helpers import _stringify_object_id, check_id
from .update import (_add_infos, _expand_add_responses, _expand_query_degree,
                     _notify_students, _set_status, _update_event_details)


@check_id
@requires_auth
@requires_scope('student')
def add_student_attendance(id, body):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        student_record = _add_infos(body, result)
        query_details.update_one({'_id': ObjectId(id)}, {'$set': {'query.responses.' + body.get('student_address'): student_record}}, upsert=False)
        return id

@requires_auth
@requires_scope('recruiter')
def dry_run_degree(body):
    query = body.get('query')
    try:
        result = _query_degree(query.get('details'))
        return len(result.keys())
    except ValueError as e:
        return {'ERROR': str(e)}, 500

@requires_auth
@requires_scope('recruiter')
@check_id
def expand_query_degree(id, body):
    old_event = query_details.find_one({'_id': ObjectId(id)})
    if not old_event:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        expanded_result, new_result = _expand_query_degree(body, old_event['query']['results'])
        expanded_notifications = _expand_add_responses(old_event['query']['responses'], new_result)
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

@requires_auth
@requires_scope('student')
def get_queries_by_student(student_address):
    results = query_details.find({'query.results.' + student_address: {"$exists": True}})
    return _build_student_result(student_address, results)

@check_id
@requires_auth
@requires_scope('registree')
def get_rsvp(id):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        return _get_rsvp(result)

@check_id
@requires_auth
@requires_scope('registree')
def notify_students(id):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        updated_responses, students = _notify_students(result['query']['responses'])
        query_details.update_one({'_id': ObjectId(id)}, {'$set': {'query.responses': updated_responses}}, upsert=False)
        return students

@requires_auth
@requires_scope('recruiter')
def query_degree(body):
    query = body.get('query')
    try:
        query['results'] = _query_degree(query.get('details'))
        query['responses'] = _add_responses(query['results'])
        query['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        body['query'] = query
        return str(query_details.insert_one(body).inserted_id)
    except ValueError as e:
        return {'ERROR': str(e)}, 500

@requires_auth
@requires_scope('recruiter')
@check_id
def update(id, body):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        event = _update_event_details(body, result)
        query_details.update_one({'_id': ObjectId(id)}, {'$set': {'event': event}}, upsert=False)
        return _get_query(id)

@check_id
@requires_auth
@requires_scope('student')
def update_status(id, body):
    result = query_details.find_one({'_id': ObjectId(id)})
    if not result:
        return {'ERROR': 'No matching data found.'}, 409
    else:
        student_record = _set_status(body, result)
        query_details.update_one({'_id': ObjectId(id)}, {'$set': {'query.responses.' + body.get('student_address'): student_record}}, upsert=False)
        return id
