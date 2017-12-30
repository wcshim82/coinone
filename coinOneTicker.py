from coinOne import CoinOne

ACCESS_TOKEN = ''
SECRET_KEY = ''


class CoinOneTicker(CoinOne):

    PAYLOAD = ''

    def __init__(self, payload, url, token, key):
        super().__init__('https://api.coinone.co.kr/ticker', token, key)
        self.PAYLOAD = payload

    def getPayLoad(self):
        return self.PAYLOAD


if __name__ == '__main__':
    payload = {"currency": "qtum"}
    ct = CoinOneTicker(payload, 'https://api.coinone.co.kr/ticker/', ACCESS_TOKEN, SECRET_KEY)
    #Need to specify GET & POST 
    print(ct.get_result())
