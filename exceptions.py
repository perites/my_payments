from flask import render_template


class BadAPIResponse(Exception):
    code = 500

    def __str__(self):
        return "ERROR: Bad API response, please try later"

    # def __init__(self):
    #     self.message = {"message": "Bad API response, please try later"}
    #     self.code = 500
    #     super().__init__(self.message)
    # def html(self):
    #     return render_template("index_post_error.html", message="Bad API response, please try later")


class NotAuthorised(Exception):
    # def __init__(self):
    #     self.message = {"message": "ERROR: Unauthorized"}
    #     self.code = 401
    #     super().__init__(self.message)
    code = 401

    def __str__(self):
        return "ERROR: Unauthorized"


class WrongCurrency(Exception):
    code = 500

    def __str__(self):
        return "ERROR: Wrong currency, please check if correct"
    # def __init__(self):
    #     self.message = {
    #         "message": "Wrong currency, please check if correct"}
    #     self.code = 500
    #     super().__init__(self.message)


class MissingArguments(Exception):
    code = 500

    def __str__(self):
        return "ERROR: Please specify amount and currency"
    # def __init__(self):
    #     self.message = {
    #         "message": "Please specify amount and currency"}
    #     self.code = 500
    #     super().__init__(self.message)
