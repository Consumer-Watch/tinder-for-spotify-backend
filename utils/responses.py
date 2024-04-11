from typing import Any
from flask import jsonify

def success_response(data: Any, status_code: int = 200):
    return jsonify({
        "success": True,
        "message": "OK",
        "data": data
    }), status_code

def error_response(status_code: int = 500, message: str = "An error occured"):
    return jsonify({
        "success": False,
        "message": message,
        "data": None
    }), status_code