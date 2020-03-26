import datetime
import json
import re

import httpretty
import pytest
from freezegun import freeze_time

from src.swagger_server.controllers.query_db_functions import (
    _add_infos, _add_responses, _build_student_result, _compute_ratios,
    _expand_add_responses, _expand_query, _get_rsvp, _notify_students, _query,
    _set_status, _update_event_details)


@httpretty.activate
def test_query():

    httpretty.register_uri(
        httpretty.POST,
        re.compile("http://.*"),
        content_type='application/json',
        body=json.dumps(_get_short_response())
    )

    details = [{
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
        "absolute": 2
    },
    {
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfb",
        "absolute": 2
    }]

    expected_output = _get_query_result()
    assert(_query(details, '12345') == expected_output)

@httpretty.activate
def test_query_fail():

    httpretty.register_uri(
        httpretty.POST,
        re.compile("http://.*"),
        content_type='application/json',
        status=408
    )

    details = [{
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
        "absolute": 2
    }]

    with pytest.raises(ValueError, match='Query not possible, status code: 408'):
        _query(details, '12345')

def test_add_responses():
    result = _get_query_result()
    expected_output = {
        "0x857979Af25b959cDF1369df951a45DEb55f2904d" : {
            "sent": "",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799240": {
            "sent": "",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0x857979Af25b959cDF1369df951a45DEb55f2904e" : {
            "sent": "",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799241": {
            "sent": "",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        }
    }
    assert(_add_responses(result) == expected_output)

@freeze_time("2012-01-01 16:00")
def test_set_status_viewed():
    body = {
        "id": "12345",
        "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904d",
        "viewed": True
    }
    result = _get_event()
    expected_output = {
        "sent": "2012-01-01 14:00",
        "viewed": "2012-01-01 16:00",
        "responded": "",
        "accepted": False,
        "attended": False
    }
    assert(_set_status(body, result) == expected_output)

@freeze_time("2012-01-01 16:01")
def test_set_status_accepted_true():
    body = {
        "id": "12345",
        "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904d",
        "accepted": True
    }
    result = _get_event()
    expected_output = {
        "sent": "2012-01-01 14:00",
        "viewed": "",
        "responded": "2012-01-01 16:01",
        "accepted": True,
        "attended": False
    }
    assert(_set_status(body, result) == expected_output)

@freeze_time("2012-01-01 16:01")
def test_set_status_accepted_false():
    body = {
        "id": "12345",
        "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904d",
        "accepted": False
    }
    result = _get_event()
    expected_output = {
        "sent": "2012-01-01 14:00",
        "viewed": "",
        "responded": "2012-01-01 16:01",
        "accepted": False,
        "attended": False
    }
    assert(_set_status(body, result) == expected_output)

def test_set_status_attended_true():
    body = {
        "id": "12345",
        "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799240",
        "student_id": "DOEJOH001",
        "first_name": "John",
        "last_name": "Doe"
    }
    result = _get_event()
    expected_output = {
        "sent": "2012-01-01 14:00",
        "viewed": "2012-01-01 15:00",
        "responded": "2012-01-01 15:01",
        "accepted": True,
        "attended": True,
        "student_info": {
            "student_id": "DOEJOH001",
            "first_name": "John",
            "last_name": "Doe"
        }
    }
    assert(_add_infos(body, result) == expected_output)

def test_compute_ratio():
    event = _get_event()
    event['query']['metrics'] = {
        'viewed': 1, 
        'responded': 1, 
        'accepted': 1,
        'attended': 0
    }
    expected_output = [event]
    results = [_get_event()]
    assert(_compute_ratios(results) == expected_output)

def test_update_event_details():
    result = _get_event_details()
    body = {
        'type': 'recruiting',
        'message': 'Hi there!'
    }
    expected_output = _get_event_details().get('event')
    expected_output['type'] = 'recruiting'
    expected_output['message'] = 'Hi there!'
    assert(_update_event_details(body, result) == expected_output)

def test_build_student_result():
    query_result = _get_query()
    expected_output = [{'_id': '5c89d28c42b09700010413f2',
        'customer_id': '123456789',
        'event': {'address': 'string',
        'end_date': 'string',
        'flyer': 'string',
        'info': 'string',
        'message': 'string',
        'name': 'string',
        'start_date': 'string',
        'type': 'string'},
        'response': {'sent': '2019-03-14 04:03',
        'viewed': '',
        'responded': '',
        'accepted': False,
        'attended': False},
        'timestamp': '2019-03-14 04:03',
        'qr': '{"query_id": "5c89d28c42b09700010413f2", "student_address": "0xDFc14F1E02A00244593dB12f53910C231eEFECAd"}'}]
    assert(_build_student_result('0xDFc14F1E02A00244593dB12f53910C231eEFECAd', query_result) == expected_output)

@httpretty.activate
def test_expand_query():

    httpretty.register_uri(
        httpretty.POST,
        re.compile("http://.*"),
        content_type='application/json',
        body=json.dumps(_get_long_response())
    )

    details = [{
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
        "absolute": 3
    },
    {
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfb",
        "absolute": 3
    }]

    expected_output = _get_long_query_result()
    assert(_expand_query(details, _get_query_result(), '12345', ) == expected_output)

def test_expand_add_responses():
    result = _get_long_query_result()
    old_notifications = {
        "0x857979Af25b959cDF1369df951a45DEb55f2904d" : {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799240": {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0x857979Af25b959cDF1369df951a45DEb55f2904e" : {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799241": {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        }
    }

    expected_output = {
        "0x857979Af25b959cDF1369df951a45DEb55f2904d" : {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799240": {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0x857979Af25b959cDF1369df951a45DEb55f2904e" : {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799241": {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799480": {
            "sent": "",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799481": {
            "sent": "",
            "viewed": "",
            "responded": "",
            "accepted": False,
            "attended": False
        }
    }
    assert(_expand_add_responses(old_notifications, result) == expected_output)

def test_get_rsvp():
    assert(_get_rsvp(_get_query()[0]) == 0)
    assert(_get_rsvp(_get_event()) == 1)

@freeze_time("2019-03-14 04:03")
def test_notify_students():
    responses = {'0x38b9118Fb0d7db10321eBffC694b946eF1CB37c5': {'sent': '',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False},
                '0x379510a728aA9269607f7037FFcbDe4c6d539f47': {'sent': '',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False},
                '0xDFc14F1E02A00244593dB12f53910C231eEFECAd': {'sent': '',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False}}
    expected_students = [
        '0x38b9118Fb0d7db10321eBffC694b946eF1CB37c5',
        '0x379510a728aA9269607f7037FFcbDe4c6d539f47',
        '0xDFc14F1E02A00244593dB12f53910C231eEFECAd'
    ]
    updated_responses, students = _notify_students(responses)
    assert(students == expected_students)
    assert (updated_responses == _get_query()[0]['query']['responses'])

def _get_short_response():
    return {
        0: [{
            "avg": 75.42233333333334,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904d",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 73.605,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799240",
            "timestamp": "2019-02-12 05:05"
        }],
        1: [{
            "avg": 81,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904e",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 79,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799241",
            "timestamp": "2019-02-12 05:05"
        }]
    }

def _get_long_response():
    return {
        0: [{
            "avg": 75.42233333333334,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904d",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 73.605,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799240",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 71,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799480",
            "timestamp": "2019-02-12 05:05"
        }],
        1: [{
            "avg": 81,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904e",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 79,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799241",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 77,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799481",
            "timestamp": "2019-02-12 05:05"
        }]
    }

def _get_query_result():
    return [{
            "avg": 75.42233333333334,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904d",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 73.605,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799240",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 81,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904e",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 79,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799241",
            "timestamp": "2019-02-12 05:05"
        }]

def _get_long_query_result():
    return [
        {
            "avg": 75.42233333333334,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904d",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 73.605,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799240",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 81,
            "complete": False,
            "student_address": "0x857979Af25b959cDF1369df951a45DEb55f2904e",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 79,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799241",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 71,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799480",
            "timestamp": "2019-02-12 05:05"
        },
        {
            "avg": 77,
            "complete": False,
            "student_address": "0xDBEd414a980d757234Bfb2684999afB7aE799481",
            "timestamp": "2019-02-12 05:05"
        }
    ]

def _get_event():
    return {
        "query": {
            "responses": {
                "0x857979Af25b959cDF1369df951a45DEb55f2904d" : {
                    "sent": "2012-01-01 14:00",
                    "viewed": "",
                    "responded": "",
                    "accepted": False,
                    "attended": False
                },
                "0xDBEd414a980d757234Bfb2684999afB7aE799240": {
                    "sent": "2012-01-01 14:00",
                    "viewed": "2012-01-01 15:00",
                    "responded": "2012-01-01 15:01",
                    "accepted": True,
                    "attended": False
                }
            }
        }
    }

def _get_event_details():
    return {
        "event": {
            "type": "showcase",
            "name": "Company XYZ Showcase",
            "start_date": "2019-02-01T10:00Z",
            "address": "1234 Main St, Cool City, CA 98765",
            "info": "The event is only for the tallest students.",
            "flyer": "https://ipfs.io/ipfs/QmTkzDwWqPbnAh5YiV5VwcTLnGdwSNsNTn2aDxdXBFca7D/example#/ipfs/QmTDMoVqvyBkNMRhzvukTDznntByUNDwyNdSfV8dZ3VKRC/readme.md",
            "message": "Hello World!"
        }
    }

def _get_query():
    return [{'_id': '5c89d28c42b09700010413f2',
        'customer_id': '123456789',
        'event': {'address': 'string',
        'end_date': 'string',
        'flyer': 'string',
        'info': 'string',
        'message': 'string',
        'name': 'string',
        'start_date': 'string',
        'type': 'string'},
        'query': {
            'details': [{'absolute': 3,
                'degree_id': '5116f8681bb7d9d768cdf8c2a2d14de99c7401e90524596a1a85e1f7a11d742b',
                'degree_name': 'string',
                'faculty_id': '2be196098241d7cf29b422517a1f55ba7ef55c5003ff0bcb901463842e2ee7c9',
                'faculty_name': 'string',
                'university_id': '6835a0287d1c818cbb8811a8c4acf81edd85726c5faa8a0047f7ea3c29e97c36',
                'university_name': 'string'}],
            'results': [
                {'avg': 64.91766666666666,
                'complete': False,
                'student_address': '0x379510a728aA9269607f7037FFcbDe4c6d539f47',
                'timestamp': '2019-02-26 10:26'},
                {'avg': 64.36633333333334,
                'complete': False,
                'student_address': '0xDFc14F1E02A00244593dB12f53910C231eEFECAd',
                'timestamp': '2019-02-26 10:26'}],
            'responses': {'0x38b9118Fb0d7db10321eBffC694b946eF1CB37c5': {'sent': '2019-03-14 04:03',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False},
                '0x379510a728aA9269607f7037FFcbDe4c6d539f47': {'sent': '2019-03-14 04:03',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False},
                '0xDFc14F1E02A00244593dB12f53910C231eEFECAd': {'sent': '2019-03-14 04:03',
                'viewed': '',
                'responded': '',
                'accepted': False,
                'attended': False}},
            'timestamp': '2019-03-14 04:03'}
        }]
