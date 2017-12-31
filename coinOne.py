# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import logging
import time
from abc import *

import httplib2
import simplejson as json

logger = logging.getLogger("coinAnalyzer")


class CoinOne(metaclass=ABCMeta):
    ACCESS_TOKEN = ''
    SECRET_KEY = ''

    def __init__(self, url, token, key):#, config):
        self.URL = url
        self.ACCESS_TOKEN = token
        self.SECRET_KEY = key.encode('utf-8')
        #self.ACCESS_TOKEN = config['ACCESS_TOKEN']
        #self.SECRET_KEY = config['SECRET_KEY'].encode('utf-8')

    @abstractclassmethod
    def getPayLoad(self):
        pass

    @abstractclassmethod
    def getMethod(self):
        pass

    def getFullPayLoad(self):
        fullPayload = {}
        fullPayload.update(self.getPayLoad())
        fullPayload.update({
            'access_token': self.ACCESS_TOKEN,
        })
        return fullPayload

    def get_encoded_payload(self, payload):
        payload[u'nonce'] = int(time.time() * 1000)

        dumped_json = json.dumps(payload)
        encoded_json = base64.b64encode(dumped_json.encode('utf-8'))
        return encoded_json

    def get_signature(self, encoded_payload, secret_key):
        signature = hmac.new(secret_key.upper(), encoded_payload, hashlib.sha512);
        return signature.hexdigest()

    def get_response(self, url, payload):
        encoded_payload = self.get_encoded_payload(payload)
        headers = {
            'Content-type': 'application/json',
            'X-COINONE-PAYLOAD': encoded_payload,
            'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.SECRET_KEY)
        }
        http = httplib2.Http()
        ( response, content ) = http.request(self.URL, self.getMethod(), headers=headers, body=encoded_payload)
        return content

    def get_result(self):
        content = self.get_response(self.URL, self.getFullPayLoad())
        content = json.loads(str(content.decode("utf-8")).replace('“', '"').replace('”', '"'))
        return content