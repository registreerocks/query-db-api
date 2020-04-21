import datetime
import json
from os import environ as env

import requests

from .query import _query_bulk


def _add_responses(query_results):
    responses = {}
    for student_address, _ in query_results.items():
        responses[student_address] = {
            'sent': '',
            'viewed': '',
            'responded': '',
            'accepted': False,
            'attended': False
        }
    return responses

def _build_query(_type, details):
    query_list = []
    id_to_name = {}
    for item in details:
        type_id = item.get(_type + '_id')
        query_list.append({
            'type': _type,
            'type_id': type_id,
            'x': item.get('absolute', 0) | item.get('percentage', 0),
            'absolute': True if item.get('absolute', 0) > item.get('percentage', 0) else False
        })
        id_to_name[type_id] = item.get(_type + '_name')
    return query_list, id_to_name

def _query_degree(details):
    query_list, id_to_degree_name = _build_query('degree', details)
    query_response = _query_bulk(query_list)
    query_results = {}
    for degree_id, response in query_response.items():
        query_results = {**query_results, **{student_address: {**value, **{'degree_name': id_to_degree_name[degree_id]}} for student_address, value in response.items()}}
    return query_results