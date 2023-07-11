from flask import Flask, request, jsonify
import logging
from exceptions import NotAuthorised
import confg
from work_with_db import Partner, Payment, Rate, get_rates, verification
from peewee import *


import json

app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e29b6b'


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='payments.log', filemode='w', level=logging.INFO)


@app.route("/history")
def see_history():
    try:

        headers = request.headers
        token = headers.get("Token")

        partner = verification(token)
        payments = Payment.select().where(Payment.owner == partner.id)

        currency = request.args.get("currency")
        logging.info(f"Searching history with filtr {currency}")

        if not currency:

            answer = [payment.to_json() for payment in payments]
            return jsonify(answer), 200

        if currency not in confg.currencys:
            return jsonify({"message": "Wrong currency, please check if correct"}), 500

        # payments = Payment.select().where(Payment.owner == partner.id and Payment.original_currency == currency)
        # payments = [x for x in payments if x.original_currency == currency]
        payments = payments.where(Payment.original_currency == currency)

        answer = [payment.to_json() for payment in payments]

        return jsonify(answer), 200

    except NotAuthorised as e:
        return e.message

    except Exception as e:
        logging.error(f"Error occured : {e}")
        return jsonify({"Error": e}), 500


@app.route("/add-payment")
def add_payment():
	try: 
		headers = request.headers
		token = headers.get("Token")
		partner = verification(token)

		currency = request.args.get("currency")
		amount = request.args.get("amount")
		logging.info(f"Got {currency} and {amount}, procesing")

		if not amount or not currency:
		    return jsonify({"message": "Please specify amount and currency"}), 500

		if currency not in confg.currencys:
		    return jsonify({"message": "Wrong currency, please check if correct"}), 500

		amount = float(amount)
		rates = get_rates()
		cal_amount = round(amount*float(rates[currency])+amount*float(rates[currency])*float(partner.partner_rate), 2)

		Payment.create(owner=partner, amount=cal_amount, original_currency=currency, original_amount=amount)
		return jsonify({"message": f"All went good, added payment at {cal_amount} hrn"}), 200


	except NotAuthorised as e:
		return e.message

	except Exception as e:
		logging.error(f"Error occured : {e}")
		return jsonify({"Error": str(e)}), 500    




@app.route("/rate")
def rate():
    try:
        headers = request.headers
        token = headers.get("Token")

        currency = request.args.get("currency")
        amount = request.args.get("amount")
        logging.info(f"Got {currency} and {amount}, procesing")

        partner = verification(token)

        if not amount or not currency:
            return jsonify({"partner_rate": partner.partner_rate}), 200

        if currency not in confg.currencys:
            return jsonify({"message": "Wrong currency, please check if correct"}), 500

        amount = float(amount)
        rates = get_rates()

        return jsonify(round(amount*float(rates[currency])+amount*float(rates[currency])*float(partner.partner_rate), 2)), 200

    except NotAuthorised as e:
        return e.message

    except Exception as e:
        logging.error(f"Error occured : {e}")
        return jsonify({"Error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
