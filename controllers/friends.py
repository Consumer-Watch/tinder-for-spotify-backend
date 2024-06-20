from models.friends import FriendRequestStatus, FriendRequests
from config.database import db


def add_friend(sender: str, receiver: str):
    existing_request = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver
    ).one_or_none()

    if existing_request is None:
        new_request = FriendRequests(
            user_id = sender,
            friend_id = receiver,
            status = FriendRequestStatus.pending
        )
        db.session.add(new_request)
        db.session.commit()
        return { **new_request.toDict(), "status": new_request.toDict()["status"].value }
    
    return { **existing_request.toDict(), "status": existing_request.toDict()["status"].value }

def accept_request(sender: str, receiver: str):
    existing_request = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver
    ).update(
        status = FriendRequestStatus.accepted
    )
    return existing_request #number of rows affected

def reject_request(sender: str, receiver: str):
    existing_request = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver
    ).update(
       status = FriendRequestStatus.rejeted
    )
    return existing_request #number of rows affected

def block_friend(sender: str, receiver: str):
    request_1 = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver,
    ).update(
       status = FriendRequestStatus.rejeted
    )

    if request_1 == 1:
        return request_1

    request_2 = FriendRequests.query.filter_by(
        friend_id = sender,
        user_id = receiver
    ).update(
       status = FriendRequestStatus.rejeted
    )
    return request_2 #number of rows affected

