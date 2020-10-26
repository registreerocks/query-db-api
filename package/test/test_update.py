import json
import re

import mock
from freezegun import freeze_time

from src.swagger_server.controllers.update import (_add_infos,
                                                   _expand_add_responses,
                                                   _expand_query_degree,
                                                   _notify_students,
                                                   _query_degree, _set_status,
                                                   _update_event_details)

from .helpers import (_get_event, _get_event_details, _get_long_query_result,
                      _get_long_response, _get_query, _get_query_result)


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

@mock.patch('src.swagger_server.controllers.update._query_degree')
def test_expand_query(query_result):
    query_result.return_value = _get_long_query_result()

    details = [{
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
        "absolute": 3,
        "degree_name": "Fintech"
    },
    {
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfb",
        "absolute": 3,
        "degree_name": "Statistics"
    }]

    expected_output = ({
      "0x857979Af25b959cDF1369df951a45DEb55f2904d": {
        "avg": 75.42233333333334,
        "complete": False,
        "timestamp": "2019-02-12 05:05",
        "degree_name": "Fintech",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
      },
      "0xDBEd414a980d757234Bfb2684999afB7aE799240": {
        "avg": 73.605,
        "complete": False,
        "timestamp": "2019-02-12 05:05",
        "degree_name": "Fintech",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
      },
      "0x857979Af25b959cDF1369df951a45DEb55f2904e": {
        "avg": 81,
        "complete": False,
        "timestamp": "2019-02-12 05:05",
        "degree_name": "Statistics",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfb",
      },
      "0xDBEd414a980d757234Bfb2684999afB7aE799241": {
        "avg": 79,
        "complete": False,
        "timestamp": "2019-02-12 05:05",
        "degree_name": "Statistics",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfb",
      },
      "0xDBEd414a980d757234Bfb2684999afB7aE799480": {
        "avg": 71,
        "complete": False,
        "timestamp": "2019-02-13 05:05",
        "degree_name": "Fintech",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
      },
      "0xDBEd414a980d757234Bfb2684999afB7aE799481": {
        "avg": 77,
        "complete": False,
        "timestamp": "2019-02-13 05:05",
        "degree_name": "Statistics",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfb",
      }
    }, _get_long_query_result())
    assert(_expand_query_degree(details, _get_query_result()) == expected_output)

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
        "student_number": "DOEJOH001",
        "user_id": "Safire|1234567890"
    }
    result = _get_event()
    expected_output = {
        "sent": "2012-01-01 14:00",
        "viewed": "2012-01-01 15:00",
        "responded": "2012-01-01 15:01",
        "accepted": True,
        "attended": True,
        "student_info": {
            "student_number": "DOEJOH001",
            "user_id": "Safire|1234567890"
        }
    }
    assert(_add_infos(body, result) == expected_output)

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
