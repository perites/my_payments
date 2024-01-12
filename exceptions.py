class BadAPIResponse(Exception):
    code = 500

    def __str__(self):
        return "ERROR: Bad API response, please try later"


class NotAuthorised(Exception):
    code = 401

    def __str__(self):
        return "ERROR: Unauthorized"


class WrongCurrency(Exception):
    code = 500

    def __str__(self):
        return "ERROR: Wrong currency, please check if correct"


class MissingArguments(Exception):
    code = 500

    def __str__(self):
        return "ERROR: Please specify amount and currency"
