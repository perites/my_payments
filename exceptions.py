from flask import Flask, render_template


class BadAPIResponse(Exception):
    def html(self):
        return render_template("index_post_error.html", message="Bad API response, please try later")


class NotAuthorised(Exception):
	def __init__(self):
		self.message =  {"message": "ERROR: Unauthorized"}, 401
		super().__init__(self.message)


