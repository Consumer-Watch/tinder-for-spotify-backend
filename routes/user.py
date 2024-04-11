from config.app import app
from flask import request
from controllers.user import get_user

@app.route('/users/<id>')
def users_route(id: str, methods=["GET", "PUT", "DELETE"]):
    if request.method == "GET":
        return get_user(id)