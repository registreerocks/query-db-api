from src.swagger_server.controllers.get import (_build_customer_result,
                                                _build_registree_result,
                                                _build_student_result,
                                                _compute_ratios, _get_rsvp)

from .helpers import _get_event, _get_query

def test_build_customer_result():
    query_result = _get_query()
    expected_output = query_result.copy()
    expected_output[0]['query']['metrics'] = {
        'viewed': 0, 
        'responded': 0, 
        'accepted': 0,
        'attended': 0
    }
    assert(_build_customer_result(query_result) == expected_output)

def test_build_registree_result():
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
        'query': {
            'details': [{'absolute': 3,
                'degree_id': '5116f8681bb7d9d768cdf8c2a2d14de99c7401e90524596a1a85e1f7a11d742b',
                'degree_name': 'string',
                'faculty_id': '2be196098241d7cf29b422517a1f55ba7ef55c5003ff0bcb901463842e2ee7c9',
                'faculty_name': 'string',
                'university_id': '6835a0287d1c818cbb8811a8c4acf81edd85726c5faa8a0047f7ea3c29e97c36',
                'university_name': 'string'}],
            'metrics': {
                'viewed': 0, 
                'responded': 0, 
                'accepted': 0,
                'attended': 0
            },
            'timestamp': '2019-03-14 04:03'}
        }]
    assert(_build_registree_result(query_result) == expected_output)



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
    expected_output = {
        'viewed': 1, 
        'responded': 1, 
        'accepted': 1,
        'attended': 0
    }
    assert(_compute_ratios(event.get('query').get('responses')) == expected_output)

def test_get_rsvp():
    assert(_get_rsvp(_get_query()[0]) == 0)
    assert(_get_rsvp(_get_event()) == 1)
