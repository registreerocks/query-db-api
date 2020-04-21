import json
import re

import mock
import pytest

from src.swagger_server.controllers.create import _add_responses, _query_degree, _query_bulk
from .helpers import _get_short_response, _get_query_result


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

@mock.patch('src.swagger_server.controllers.create._query_bulk')
def test_query_degree(query_result):
    query_result.return_value = _get_short_response()

    details = [{
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfa",
        "degree_name": "Fintech",
        "absolute": 2
    },
    {
        "university_id": "3f98f095ef1a7b782d9c897d8d004690d598ebe4c301f14256366beeaf083365",
        "degree_id": "7c9a1789f207659f2a28ee16737946d6b4189cb507ddd0fedc92978acaba4dfb",
        "degree_name": "Statistics",
        "absolute": 2
    }]

    expected_output = _get_query_result()
    assert(_query_degree(details) == expected_output)