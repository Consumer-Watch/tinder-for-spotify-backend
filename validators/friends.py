from flask import Request

from utils.responses import error_response

def get_from_body(request: Request):
    sender = request.get_json().get('user_id', None)
    receiver = request.get_json().get('friend_id', None)
    return (sender, receiver)

def get_from_params(request: Request):
    sender = request.args.get('user_id', None)
    receiver = request.args.get('friend_id', None)
    return (sender, receiver)


def validate_friend_request(request: Request):
    sender, receiver = get_from_body(request)

    if sender is None or receiver is None:
        return error_response(400, "user_id or friend_id must be in request body")

    if sender == '' or receiver == '':
        return error_response(400, "user_id or friend_id must be in request body")

    if sender == receiver:
        return error_response(400, 'user_id and friend_id cannot be the same')
    
    return (sender, receiver)

def validate_friend_request_params(request: Request):
    sender, receiver = get_from_params(request)

    if sender is None or receiver is None:
        return error_response(400, "user_id or friend_id must be in request query")

    if sender == '' or receiver == '':
        return error_response(400, "user_id or friend_id must be in request query")

    if sender == receiver:
        return error_response(400, 'user_id and friend_id cannot be the same')
    
    return (sender, receiver)


