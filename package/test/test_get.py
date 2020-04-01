from src.swagger_server.controllers.get import (_build_student_result,
                                                _compute_ratios, _get_rsvp)

from .helpers import _get_event, _get_query


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

def test_get_rsvp():
    assert(_get_rsvp(_get_query()[0]) == 0)
    assert(_get_rsvp(_get_event()) == 1)
