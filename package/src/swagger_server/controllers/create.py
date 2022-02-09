import datetime
import json
from os import environ as env

import requests

from .query import _query_bulk
from .helpers import _get_student_details


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
            'x': item.get('absolute', 0) | item.get('percentage', 0) | item.get('average', 0),
            'absolute': True if item.get('absolute', 0) > item.get('percentage', 0) | item.get('average', 0) else False,
            'average': True if item.get('average', 0)  > item.get('percentage', 0) | item.get('absolute', 0) else False
        })
        id_to_name[type_id] = item.get(_type + '_name')
    return query_list, id_to_name

def _query_degree(details):
    query_list, id_to_degree_name = _build_query('degree', details)
    query_response = _query_bulk(query_list)
    race_query = _get_first_not_none([y.get('race') for y in details])
    gender_query = _get_first_not_none([y.get('gender') for y in details])
    filtered_response = _filter_results_by_demographics(race_query,
                                                        gender_query,
                                                        query_response)
    query_results = {}
    for degree_id, response in filtered_response.items():
        query_results = {**query_results, **{student_address: {**value, **{'degree_id': degree_id, 'degree_name': id_to_degree_name[degree_id]}} for student_address, value in response.items()}}
    return query_results


def _filter_results_by_demographics(race_query, gender_query, query_response):
    # Don't filter on demographics if no demographic filters is included
    if not race_query and not gender_query:
        return query_response

    addresses = [address for students in query_response.values() for address in students]
    student_details = _get_student_details(addresses)

    if race_query:
        student_details = _filter_by_race(student_details, race_query)
    if gender_query:
        student_details = _filter_by_gender(student_details, gender_query)

    filtered_ids = [student['_id'] for student in student_details]

    return {degree_id:
            {student_addr: student_res
             for student_addr, student_res in responses.items()
             if student_addr in filtered_ids}
            for degree_id, responses in query_response.items()}


def _get_first_not_none(array):
    return next((item for item in array if item is not None), False)

def _filter_by_race(student_details, races):
    return _filter_details_by_demographic(student_details, races, 'race')


def _filter_by_gender(student_details, genders):
    return _filter_details_by_demographic(student_details, genders, 'gender')


def _filter_details_by_demographic(student_details, demographics, demographic_type):
    return [student for student in student_details if student['ident'][0]
            .get(demographic_type, "Other") in demographics]
