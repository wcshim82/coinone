import json
import time
import base64
import hashlib
import hmac

ACCESS_TOKEN = ''
SECRET_KEY = ''
APIURL = 'https://api.coinone.co.kr'

def get_encoded_payload(payload):
    #add nonce
    payload[u'nonce'] = int(time.time()*1000)
    dumped_json = json.dumps(payload)
    encoded_json = base64.b64encode(dumped_json)
    return encoded_json


def get_signature(encoded_payload, secret_key):
    signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
    return signature.hexdigest()


def get_response(url, payload):
    encoded_payload = get_encoded_payload(payload)
    response = client.post(APIURL + url,
                           format='json',
                           data=encoded_payload,
                           **{
                               'X-COINONE-PAYLOAD': encoded_payload,
                               'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
                           })
    return response


def get_balance():
    url = '/balance'
    payload = {
        'access_token': ACCESS_TOKEN,
    }
    response = get_response(url, payload)
    content = json.loads(response.content)
    return content


if __name__   == "__main__":
    print get_balance()