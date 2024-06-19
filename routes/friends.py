from config.app import app
from flask import request

from controllers.friends import accept_request, add_friend, block_friend, reject_request
from utils.responses import error_response, success_response
from validators.friends import validate_friend_request

@app.route('/friends/add', methods=["POST"])
def make_friend_request():
    sender, receiver = validate_friend_request(request)

    try:
        friend_request = add_friend(sender, receiver)
        return success_response(friend_request, 201)
    except Exception as error:
        return error_response(500, str(error))


@app.route('/friends/accept', methods=["PUT"])
def accept_friend_request():
    sender, receiver = validate_friend_request(request)

    try:
        affected_rows = accept_request(sender, receiver)
        if affected_rows < 1:
            return error_response(404, "Friend Request record nto found")
        
        return success_response(None, 200)
    except Exception as error:
        return error_response(500, str(error))

@app.route('/friends/reject', methods=["PUT"])
def reject_friend_request():
    sender, receiver = validate_friend_request(request)

    try:
        affected_rows = reject_request(sender, receiver)
        if affected_rows < 1:
            return error_response(404, "Friend Request record nto found")
        
        return success_response(None, 200)
    except Exception as error:
        return error_response(500, str(error))
    

@app.route('/friends/block', methods=["PUT"])
def block_user():
    sender, receiver = validate_friend_request(request)

    try:
        affected_rows = block_friend(sender, receiver)
        if affected_rows < 1:
            return error_response(404, "Friend Request record nto found")
        
        return success_response(None, 200)
    except Exception as error:
        return error_response(500, str(error))


