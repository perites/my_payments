import logging

from flask import jsonify
from functools import wraps


def error_catcher(func):
    @wraps(func)
    def wrapper():
        try:
            data, code = func()
            return jsonify({"data": data}), code
        except Exception as e:
            logging.error(f"Error occured : {e}")
            return jsonify({"data": e.__str__()}), e.code if hasattr(e, "code") else 500

    return wrapper
