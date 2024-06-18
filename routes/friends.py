from config.app import app
from flask import request

from controllers.friends import add_friend
from utils.responses import error_response, success_response

@app.route('/friends/add', methods=["POST"])
def make_friend_request():
    sender = request.get_json().get('user_id', None)
    receiver = request.get_json().get('friend_id', None)

    if sender is None or receiver is None:
        return error_response(400, "user_id or friend_id must be in request body")

    if sender == '' or receiver == '':
        return error_response(400, "user_id or friend_id must be in request body")

    if sender == receiver:
        return error_response(400, 'user_id and friend_id cannot be the same')
    try:
        friend_request = add_friend(sender, receiver)
        return success_response(friend_request, 201)
    except Exception as error:
        return error_response(500, str(error))
