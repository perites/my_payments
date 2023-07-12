import requests
import logging
from exceptions import BadAPIResponse
import json


class PrivatAPI():
    response = None

    def get_privat_api(self):
        response = requests.get(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")
        logging.info(f"Getting api for privat")
        if response.status_code == 200:
            PrivatAPI.response = response
        else:
            raise BadAPIResponse


class UsdAPI(PrivatAPI):
    def get_rate(self):
        if not PrivatAPI.response:
            self.get_privat_api()
        return float(PrivatAPI.response.json()[1]["sale"])


class EuroAPI(PrivatAPI):
    def get_rate(self):
        if not PrivatAPI.response:
            self.get_privat_api()

        return float(PrivatAPI.response.json()[0]["sale"])


class CryptoAPI():
    response = None

    def get_crypto_api(self):
        with open("response.json", "r") as answer_file:
            CryptoAPI.response = json.load(answer_file)


class EthAPI(CryptoAPI):
    def get_rate(self):
        if not CryptoAPI.response:
            self.get_crypto_api()

        return CryptoAPI.response[1]["rate"] * UsdAPI().get_rate()


class BtcAPI(CryptoAPI):
    def get_rate(self):
        if not CryptoAPI.response:
            self.get_crypto_api()

        return CryptoAPI.response[0]["rate"] * UsdAPI().get_rate()


class HrnAPI():
    def get_rate(self):
        return 1
