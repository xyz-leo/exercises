# helpers.py

from flask import jsonify

# Standard JSON response helper function with success flag, message, data, and status code
def send_response(data=None, msg="", status=200, success=True):
    return jsonify({
        'success': success,     # Boolean indicating if operation succeeded
        'message': msg,         # Message to send to client
        'data': data            # Payload (usually serialized object or list)
        }), status              # HTTP status code returned alongside JSON


# Check if any required fields are missing from the request data dictionary
def missing_fields(req_fields, data):
    missing = [f for f in req_fields if f not in data]  # List comprehension for missing keys
    return missing if missing else None                  # Return list or None if all present


# Retrieve a database object by ID and model class (returns None if not found)
def find_by_id(obj_id, model):
    return model.query.get(obj_id)


# Serialize a single database object into a dictionary for JSON output
def serialize_obj(obj):
   return {
            'id': obj.id,
            'title': obj.title,
            'description': obj.description,
            'created_at': obj.created_at   # datetime object, will be serialized by jsonify
            }


# Serialize a list of database objects into list of dictionaries
def serialize_obj_list(obj_list):
    serialized_list = [serialize_obj(o) for o in obj_list if o]  # Filter out any None objects
    return serialized_list

