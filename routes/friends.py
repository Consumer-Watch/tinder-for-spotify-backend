from config.app import app
from flask import request

from controllers.friends import accept_request, add_friend, block_friend, check_friend_status, list_friend_requests, reject_request
from controllers.user import update_user
from models.user import User
from utils.responses import error_response, success_response
from validators.friends import validate_friend_request, validate_friend_request_params

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
            return error_response(404, "Friend Request record not found")
        
        #Perform these in parallel
        update_user(sender, { "friend_count": User.friend_count + 1 })
        update_user(receiver, { "friend_count": User.friend_count + 1 })

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
    

@app.route('/friends/check', methods=["GET"])
def check_friends():
    sender, receiver = validate_friend_request_params(request)

    try:
        is_friend = check_friend_status(sender, receiver)
        
        return success_response({ "is_friend": is_friend }, 200)
    except Exception as error:
        return error_response(500, str(error))
    

@app.route('/friends/requests', methods=["GET"])
def get_friend_requests():
    user_id = request.args.get('user_id', None)

    if user_id is None or user_id == "":
        return error_response(400,  "user_id not present in query string")
    
    try:
        friend_requests = list_friend_requests(user_id)
        return success_response(friend_requests)
    except Exception as e:
        return error_response(500, str(e))


