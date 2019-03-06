import datetime
import json
import re

import httpretty
import pytest
import requests
from freezegun import freeze_time

from src.swagger_server.controllers.query_db_functions import (_compute_ratios,
                                                               _notify_students,
                                                               _query,
                                                               _set_status,
                                                               _update_event_details)


@httpretty.activate
def test_query():
    response_data = [{
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
    }]
    json_data = json.dumps(response_data)

    httpretty.register_uri(
        httpretty.GET,
        re.compile("http://.*"),
        content_type='application/json',
        body=json_data
    )

    details = [{
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
        "absolute": 2
    }]

    expected_output = _get_query_result()
    assert(_query(details, '12345') == expected_output)

@freeze_time("2012-01-01 14:00")
def test_notify_students():
    result = _get_query_result()
    expected_output = {
        "0x857979Af25b959cDF1369df951a45DEb55f2904d" : {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False
        },
        "0xDBEd414a980d757234Bfb2684999afB7aE799240": {
            "sent": "2012-01-01 14:00",
            "viewed": "",
            "responded": "",
            "accepted": False
        }
    }
    assert(_notify_students(result) == expected_output)

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
        "accepted": False
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
        "accepted": True
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
        "accepted": False
    }
    assert(_set_status(body, result) == expected_output)

def test_compute_ratio():
    event = _get_event()
    event['query']['metrics'] = {
        'viewed': 0.5, 
        'responded': 0.5, 
        'accepted': 0.5
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
    

def _get_query_result():
    return [{
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
        "course_id": None,
        "result": [{
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
        }]
    }]

def _get_event():
    return {
        "query": {
            "responses": {
                "0x857979Af25b959cDF1369df951a45DEb55f2904d" : {
                    "sent": "2012-01-01 14:00",
                    "viewed": "",
                    "responded": "",
                    "accepted": False
                },
                "0xDBEd414a980d757234Bfb2684999afB7aE799240": {
                    "sent": "2012-01-01 14:00",
                    "viewed": "2012-01-01 15:00",
                    "responded": "2012-01-01 15:01",
                    "accepted": True
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
