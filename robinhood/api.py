import json
import requests
from requests import Request, Session
import urllib.parse as url

BASE = 'https://api.robinhood.com/'
TOKEN = ''

def login(username, password):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'username': username, 'password': password
    }

    u = url.urljoin(BASE, '/api-token-auth/')
    r = requests.post(u, body, headers=headers)
    TOKEN = r.json()['token']

    print('login status: ', r.status_code)
# market order
# fill or kill

def order_buy(ticker, qty):
    pass

def now(ticker):
    u = url.urljoin(BASE, '/quotes/' + ticker + '/')
    r = requests.get(u)
    print(u)
    print(r.text)

def init(ticker):
    un = input('username: ')
    pw = input('password: ')
    login(un, pw)
