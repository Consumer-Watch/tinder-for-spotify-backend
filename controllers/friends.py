from models.friends import FriendRequestStatus, FriendRequests
from models.user import User
from config.database import db
from utils.functions import send_email_to_user
from serializers.user import user_schema


def add_friend(sender: str, receiver: str):
    existing_request = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver,
    ).one_or_none()

    existing_request_2 = FriendRequests.query.filter_by(
        user_id = receiver,
        friend_id = sender
    ).one_or_none()

    if existing_request is None and existing_request_2 is None:
        user = User.query.get({"id" : sender})
        user = user_schema.dump(user)


        receiving_user = User.query.get({"id" : receiver})
        receiving_user = user_schema.dump(receiving_user)


        new_request = FriendRequests(
            user_id = sender,
            friend_id = receiver,
            sender_username = user.get('spotify_username', ''),
            sender_avatar = user.get('profile_image', ''),
            status = FriendRequestStatus.pending
        )
        db.session.add(new_request)
        db.session.commit()

        send_email_to_user(
            "New Friend Request",
            f"{user['name']} sent you a friend request on Sonder. Open the app to check it out!",
            [receiving_user['email']]
        )
    # Select needed columns from DB
        return { **new_request.toDict(), "status": new_request.toDict()["status"].value }, 201
    
    if existing_request is None:
        return { **existing_request_2.toDict(), "status": existing_request_2.toDict()["status"].value }, 200

    if existing_request_2 is None:
        return { **existing_request.toDict(), "status": existing_request.toDict()["status"].value }, 200

def accept_request(sender: str, receiver: str):
    user = User.query.get({"id" : sender})
    user = user_schema.dump(user)


    receiving_user = User.query.get({"id" : receiver})
    receiving_user = user_schema.dump(receiving_user)

    existing_request = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver
    ).update(
        values={
            "status": FriendRequestStatus.accepted
        }
    )
    db.session.commit()

    send_email_to_user(
        "Friend Request Accepted",
        f"{receiving_user['name']} accepted your friend request on Sonder. Open the app to check it out!",
        [user['email']]
    )
    return existing_request #number of rows affected

def reject_request(sender: str, receiver: str):
    existing_request = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver
    ).update(
        values={
            "status": FriendRequestStatus.rejeted
        }
    )
    db.session.commit()
    return existing_request #number of rows affected

def block_friend(sender: str, receiver: str):
    request_1 = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver,
    ).update(
        values={
            "status": FriendRequestStatus.blocked
        }
    )

    if request_1 == 1:
        return request_1

    request_2 = FriendRequests.query.filter_by(
        friend_id = sender,
        user_id = receiver
    ).update(
        values={
            "status": FriendRequestStatus.rejeted
        }
    )
    db.session.commit()
    return request_2 #number of rows affected

def check_friend_status(sender: str, receiver: str):
    request_1 = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver,
        status = FriendRequestStatus.accepted
    ).one_or_none()

    if request_1 is not None:
        return True

    request_2 = FriendRequests.query.filter_by(
        friend_id = sender,
        user_id = receiver,
        status = FriendRequestStatus.accepted
    ).one_or_none()

    if request_2 is not None:
        return True
    else:
        return False


def list_friend_requests(user_id: str):
    friend_requests = FriendRequests.query.filter_by(
        friend_id = user_id,
        status = FriendRequestStatus.pending
    ).\
    all()

    friend_requests = [
       { 
            "user_id": item.toDict()["user_id"] ,
            "friend_id": item.toDict()["friend_id"],
            "sender_username": item.toDict()["sender_username"],
            "sender_avatar": item.toDict()["sender_avatar"],
            "created_at": item.toDict()["created_at"],
        } 
        for item in friend_requests
   ] 
    
    
    return friend_requests

def list_friends(user_id: str):
    friend_set_1 = db.session.query(FriendRequests).filter_by(
        user_id = user_id,
        status = FriendRequestStatus.accepted
    ).join(
        User,
        User.id == FriendRequests.friend_id
    ).with_entities(
        User.id,
        User.spotify_username,
        User.profile_image,
        User.name,
        User.bio
    ).all()
        

    friend_set_2 = db.session.query(FriendRequests).filter_by(
        friend_id = user_id,
        status = FriendRequestStatus.accepted
    ).join(
        User,
        User.id == FriendRequests.user_id
    ).with_entities(
        User.id,
        User.spotify_username,
        User.profile_image,
        User.name,
        User.bio
    ).all()


    friends = [
       { 
            "id": user_id,
            "name": name,
            "username": spotify_username,
            "profile_image": profile_image,
            "bio": bio,
        } 
        for (user_id, spotify_username, profile_image, name, bio) in friend_set_1 + friend_set_2
   ] 
    
    
    return friends
