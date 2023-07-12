from flask import render_template


class BadAPIResponse(Exception):
    def html(self):
        return render_template("index_post_error.html", message="Bad API response, please try later")


class NotAuthorised(Exception):
    def __init__(self):
        self.message = {"message": "ERROR: Unauthorized"}
        self.code = 401
        super().__init__(self.message)


class WrongCurrency(Exception):
    def __init__(self):
        self.message = {
            "message": "Wrong currency, please check if correct"}
        self.code = 500
        super().__init__(self.message)


class MissingArguments(Exception):
    def __init__(self):
        self.message = {
            "message": "Please specify amount and currency"}
        self.code = 500
        super().__init__(self.message)
