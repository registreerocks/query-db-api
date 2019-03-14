from bson import ObjectId

def check_id(f):

    def wrapper(*args, **kwargs):
        try:
            ObjectId(kwargs.get('id'))
        except:
            return {"ERROR": "Invalid id"}, 400
        return f(*args, **kwargs)

    return wrapper