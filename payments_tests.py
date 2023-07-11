import unittest
import main
import requests





class TestCurrencyRates(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/"

    def setUp(self):
        self.headers = {"Token": "aa1"}

    def test_rate_get_partners_rate(self):
        response = requests.get(self.base_url+"rate", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["partner_rate"],'0.05')

    def test_rate_with_wrong_token(self):
        headers = {"Token": "cc3"}
        response = requests.get(self.base_url+"rate", headers=headers)
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["message"], "ERROR: Unauthorized")

    def test_rate_get_with_wrong_amount(self):
        response = requests.get(self.base_url+"rate"+"?amount=ttt&currency=Usd", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["Error"],"could not convert string to float: 'ttt'")

    def test_rate_with_amount_wrong_currency(self):
        response = requests.get(self.base_url+"rate"+"?currency=Ght&amount=100", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"],'Wrong currency, please check if correct')
  
    def test_rate_get_with_currency_and_amount(self):
        response = requests.get(self.base_url+"rate"+"?currency=Usd&amount=100", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data,3906)    




    def test_history(self):
        response = requests.get(self.base_url+"history", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        print(data, "---test_history")

    def test_history_with_wrong_currency(self):
        response = requests.get(self.base_url+"history"+"?currency=Ght", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"],"Wrong currency, please check if correct")

    def test_history_with_currency(self):
        response = requests.get(self.base_url+"history"+"?currency=Usd", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        print("\n", data, "---test_history_with_currency")

    def test_history_with_wrong_token(self):
        headers = {"Token": "cc3"}
        response = requests.get(self.base_url+"history", headers=headers)
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["message"], "ERROR: Unauthorized")




    def test_add_get_partners_rate(self):
        response = requests.get(self.base_url+"add-payment", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"],"Please specify amount and currency")

    def test_add_with_wrong_token(self):
        headers = {"Token": "cc3"}
        response = requests.get(self.base_url+"add-payment", headers=headers)
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["message"], "ERROR: Unauthorized")

    def test_add_get_with_wrong_amount(self):
        response = requests.get(self.base_url+"add-payment"+"?amount=ttt&currency=Usd", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["Error"],"could not convert string to float: 'ttt'")

    def test_add_with_amount_wrong_currency(self):
        response = requests.get(self.base_url+"add-payment"+"?currency=Ght&amount=100", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"],'Wrong currency, please check if correct')
  
    def test_add_get_with_currency_and_amount(self):
        headers = {"Token": "vv12"}
        response = requests.get(self.base_url+"add-payment"+"?currency=Usd&amount=100", headers=headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"],"All went good, added payment at 3906.0 hrn")    






if __name__ == "__main__":
    unittest.main()