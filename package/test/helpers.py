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
