# from django.test import TestCase
#
import requests

token = requests.post(url='https://www.yoomoney.ru/oauth/authorize HTTP/1.1',
              headers={
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'Content-Length': '191',
                  'client_id': '13E66635AD6BFAC21FE1DF88F0ECF46D8A7BA124D99473C4784F8F5778BAF356',
                  'response_type': 'code',
                  'redirect_uri': '127.0.0.1:8000/notify',
                  'scope': 'account-info operation-history'
              }
              )
print(token)