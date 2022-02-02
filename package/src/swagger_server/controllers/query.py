import math

from .db import student_details as MDBC

def _query_bulk(query_list):
    responses = {}
    for item in query_list:
        if item.get('absolute'):
            responses[item.get('type_id')] = _get_top_x(item.get('x'), item.get('type'), item.get('type_id'))
        else:
            responses[item.get('type_id')] = _get_top_x_percent(item.get('x'), item.get('type'), item.get('type_id'))
    return responses

def _get_top_x(x, _type, _id):
    averages = _retrieve_averages(_type, _id)
    if x < len(averages):
        return dict((item.pop('student_address'), item.copy()) for item in averages[:x])
    else:
        return dict((item.pop('student_address'), item.copy()) for item in averages)

def _get_top_x_percent(x, _type, _id):
    averages = _retrieve_averages(_type, _id)
    reduced_list = _x_percent(x, averages)
    return dict((item.pop('student_address'), item.copy()) for item in reduced_list)

def _get_all_above_average(average, _type, _id):
    averages = _retrieve_averages(_type, _id)
    reduced_list = [a for a in averages if a['avg'] >= average]
    return dict((item.pop('student_address'), item.copy()) for item in reduced_list)

def _retrieve_averages(_type, _id):
    files = list(MDBC.find({'asset.data.asset_type': _type + '_average', 'asset.data.' + _type + '_id': _id}))
    return _sort_averages(files)

def _sort_averages(files):
    average_dict = {}
    for f in files:
        student_address = f['asset']['data']['student_address']
        term = f['asset']['data']['term']
        if average_dict.get(student_address, {'term': 0})['term'] <= term:
            average = f['metadata']
            average['student_address'] = student_address
            average['term'] = term
            average_dict[student_address] = average
    averages = [ v for v in average_dict.values() ]
    return sorted(averages, key=lambda k: k['avg'], reverse=True)

def _x_percent(x, sorted_averages):
    y = math.ceil(x/100 * len(sorted_averages))
    return sorted_averages[:y]
