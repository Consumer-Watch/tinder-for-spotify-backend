from models.friends import FriendRequestStatus, FriendRequests
from config.database import db


def add_friend(sender: str, receiver: str):
    existing_request = FriendRequests.query.filter_by(
        user_id = sender,
        friend_id = receiver
    ).one_or_none()
    print(existing_request.toDict())

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
    
