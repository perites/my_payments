from flask import Flask, request, jsonify
import logging
import exceptions
import confg
# import requests
from work_with_db import Partner, Payment, Rate, get_rates
from peewee import *


app = Flask(__name__)

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='payments.log', filemode='w', level=logging.INFO)


@app.route("/history")
def see_history():
    try:

        headers = request.headers
        token = headers.get("Token")

        if token not in confg.allowed_tokens:
            logging.info(f"didnt authorised  with token {token}")
            return jsonify({"message": "ERROR: Unauthorized"}), 401

        logging.info(f"authorised sucesfuly with token {token}")

        currency = request.args.get("currency")
        logging.info(f"Searching history with filtr {currency}")

        if not currency:
            query = (Partner
                     .select(Partner, Payment)
                     .join(Payment, JOIN.LEFT_OUTER)
                     .where(Partner.token == token)
                     )

            n = 1
            answer = []
            for partner in query:
                answer1 = f"Payment {n}, {partner.payment.timestamp}, {partner.payment.original_amount} {partner.payment.original_currency} was transfered to {partner.payment.amount} hrn"
                answer.append(answer1)
                n += 1

            return jsonify(answer), 200

        if currency not in confg.currencys:
            return jsonify({"message": "Wrong currency, please check if correct"}), 500

        query = (Partner
                 .select(Partner, Payment)
                 .join(Payment, JOIN.LEFT_OUTER)
                 .where(Partner.token == token)
                 .where(Payment.original_currency == currency)
                 )
        n = 1
        answer = []
        for partner in query:
            answer1 = f"Payment {n} {partner.payment.timestamp}, with currency {partner.payment.original_currency} {partner.payment.original_amount}  was transfered to {partner.payment.amount} hrn"
            answer.append(answer1)
            n += 1

        return jsonify(answer), 200

    except AttributeError as e:
        return jsonify(f"You have no payments ! : {e}"), 500


@app.route("/add-payment", methods=["POST"])
def add_payment():
    pass


@app.route("/rate")
def rate():
	try:
		headers = request.headers
		token = headers.get("Token")

		if token not in confg.allowed_tokens:
			logging.info(f"didnt authorised  with token {token}")
			return jsonify({"message": "ERROR: Unauthorized"}), 401

		logging.info(f"authorised sucesfuly with token {token}")

		currency = request.args.get("currency")
		amount = request.args.get("amount")
		logging.info(f"Got {currency} and {amount}, procesing")


		query = (Partner
				.select(Partner)
				.where(Partner.token == token)
				)

		if not amount or not currency:
			return jsonify(f"Your partner rate is {query[0].partner_rate}"), 200

		if currency not in confg.currencys:
			return jsonify({"message": "Wrong currency, please check if correct"}), 500


		amount = float(amount)
		rates = get_rates()

		return jsonify(round(amount*float(rates[currency])+amount*float(rates[currency])*float(query[0].partner_rate), 2)), 200





	except Exception as e :
		logging.error(f"error occured {e}")
		return jsonify(f"error occured : {e}"), 500

    


if __name__ == '__main__':
    app.run(debug=True)
