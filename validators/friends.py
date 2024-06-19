from flask import Request

from utils.responses import error_response


def validate_friend_request(request: Request):
    sender = request.get_json().get('user_id', None)
    receiver = request.get_json().get('friend_id', None)

    if sender is None or receiver is None:
        return error_response(400, "user_id or friend_id must be in request body")

    if sender == '' or receiver == '':
        return error_response(400, "user_id or friend_id must be in request body")

    if sender == receiver:
        return error_response(400, 'user_id and friend_id cannot be the same')
    
    return (sender, receiver)
