from lib import utils
import json
import requests

def test_sign():
    client_secret = 'O7mvc7mKab6iwHjMkk6qaYylaqSLQaNQ'
    # a = utils.random_generate_string(16)
    params = {
        'client_id': 'CXam9rlOUcOu7H8F',
        'title': 'title',
        'content': 'content',
    }
    params['sign'] = utils.get_assign(params, client_secret)
    response = requests.post(
        'http://127.0.0.1:8000/api/send_email/',
        data=params
    )
    print(params)
    print('fffffffffffffff')

test_sign()