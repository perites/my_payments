import logging

from flask import jsonify
from functools import wraps


from exceptions import NotAuthorised, WrongCurrency, MissingArguments


def error_catcher(func):
    @wraps(func)
    def wrapper():
        try:
            data, code = func()
            return jsonify({"data": data}), code

        except NotAuthorised as e:
            logging.error(f"Error occured : {e}")
            return jsonify(e.message), e.code

        except WrongCurrency as e:
            logging.error(f"Error occured : {e}")
            return jsonify(e.message), e.code

        except MissingArguments as e:
            logging.error(f"Error occured : {e}")
            return jsonify(e.message), e.code

        except Exception as e:
            logging.error(f"Error occured : {e}")
            return {"message": str(e)}, 500

    return wrapper
