import logging

from flask import Flask, request

from exceptions import WrongCurrency, MissingArguments
import confg
from work_with_db import Payment, get_rates, verification
from decorators import error_catcher

app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e29b6b'


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='payments.log', filemode='w', level=logging.INFO)


@app.route("/history")
@error_catcher
def see_history():
    headers = request.headers
    token = headers.get("Token")

    partner = verification(token)
    payments = Payment.select().where(Payment.owner == partner.id)

    currency = request.args.get("currency")
    logging.info(f"Searching history with filtr {currency}")

    if not currency:

        answer = [payment.to_json() for payment in payments]
        return answer, 200

    if currency not in confg.currencys:
        raise WrongCurrency

    payments = payments.where(Payment.original_currency == currency)

    return [payment.to_json() for payment in payments], 200


@app.route("/rate")
@error_catcher
def rate():
    headers = request.headers
    token = headers.get("Token")

    currency = request.args.get("currency")
    amount = request.args.get("amount")
    logging.info(f"Got {currency} and {amount}, procesing")

    partner = verification(token)

    if not amount or not currency:
        return {"partner_rate": partner.partner_rate}, 200

    if currency not in confg.currencys:
        raise WrongCurrency

    amount = float(amount)
    rates = get_rates()

    return {"result": round(amount * float(rates[currency]) + amount * float(rates[currency]) * float(partner.partner_rate), 2)}, 200


@app.route("/add-payment", methods=["POST"])
@error_catcher
def add_payment():
    headers = request.headers
    token = headers.get("Token")
    partner = verification(token)

    currency = request.form.get("currency")
    amount = request.form.get("amount")

    logging.info(f"Got {currency} and {amount}, procesing")

    if not amount or not currency:
        raise MissingArguments

    if currency not in confg.currencys:
        raise WrongCurrency

    amount = float(amount)
    rates = get_rates()
    cal_amount = round(amount * float(rates[currency]) + amount * float(
        rates[currency]) * float(partner.partner_rate), 2)

    new_payment = Payment.create(owner=partner, amount=cal_amount,
                                 original_currency=currency, original_amount=amount)
    logging.info(f"Added payment {new_payment.id}")
    return {"success": f"added payment {new_payment.id}"}, 200


if __name__ == '__main__':
    app.run(debug=True)
