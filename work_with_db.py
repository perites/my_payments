from peewee import *
from datetime import date, datetime
import logging
import confg
import work_with_api
import json


db = SqliteDatabase('payments_partners.db')


class Partner(Model):
    name = CharField()
    token = CharField()
    partner_rate = CharField() 

    class Meta:
        database = db


class Payment(Model):
    owner = ForeignKeyField(Partner, backref='payments')
    amount = CharField()
    timestamp = DateTimeField(default=datetime.now)
    original_amount = CharField()
    original_currency = CharField()

    class Meta:
        database = db

    def to_json(self):
    	answer_dict = {"owner id " : self.owner.name, 
    					"amount" : self.amount, 
    					"timestamp" : self.timestamp,
    					"original_amount" : self.original_amount,
    					"original_currency" : self.original_currency}

    	return answer_dict


class Rate(Model):
	date = DateTimeField()
	currency_in = CharField()
	currency_to = CharField()
	rate = CharField()

	class Meta:
		database = db



def get_rates():
	query = Rate.select().where(Rate.date == date.today())
	if not query:
		logging.info(f"No records for {date.today()}, adding")
		for cur in confg.currencys:
			rate = getattr(work_with_api, cur+"API")().get_rate()
			Rate.create(date=date.today(), currency_in=cur, currency_to="Hrn", rate=rate)
		query = Rate.select().where(Rate.date == date.today())
	else:
		logging.info(f"There is record for {date.today()} : {query[0].date} continuing")

	answer = {}
	for r in query:
		answer[r.currency_in] = r.rate
	return answer 

