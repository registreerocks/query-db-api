from bson import ObjectId

def check_id(f):

    def wrapper(*args, **kwargs):
        try:
            ObjectId(kwargs.get('id'))
            return f(*args, **kwargs)
        except:
            return {"ERROR": "Invalid id"}, 400

    return wrapper