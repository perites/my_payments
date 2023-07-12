import logging

from flask import jsonify

from exceptions import NotAuthorised, WrongCurrency, MissingArguments


def error_catcher(func):
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
            return {"Error": str(e)}, 500

    wrapper.__name__ = func.__name__
    return wrapper
