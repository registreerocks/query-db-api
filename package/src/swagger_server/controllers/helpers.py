from bson import ObjectId
from .db import identifying_db as IDB


def check_id(f):

    def wrapper(*args, **kwargs):
        try:
            ObjectId(kwargs.get('id'))
        except:
            return {"ERROR": "Invalid id"}, 400
        return f(*args, **kwargs)

    return wrapper

def _stringify_object_id(result):
    stringified_result = []
    for element in result:
        element['_id'] = str(element['_id'])
        stringified_result.append(element)
    return stringified_result

def _get_student_details(addresses):
    return list(IDB.aggregate([
        {"$match": {"_id": {"$in": addresses}}},
        {"$lookup": {"from": "identifying_db", "localField": "ident_id",
                     "foreignField": "_id", "as": "ident"}}]))
