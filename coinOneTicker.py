from coinOne import CoinOne

ACCESS_TOKEN = '8dbd5b6e-0766-4d31-9055-2dcd4f59bbc2'
SECRET_KEY = 'a8d20b44-2932-4e86-a9b3-817d1dde3b80'


class CoinOneTicker(CoinOne):
    BASEURL = 'https://api.coinone.co.kr/ticker?'
    URL = ''
    PAYLOAD = ''
    METHOD = ''

    def __init__(self):
        super().__init__(self.URL, ACCESS_TOKEN, SECRET_KEY)

    def getPayLoad(self):
        return self.PAYLOAD

    def getMethod(self):
        return self.METHOD

    def getPrice(self, currency):
        self.URL = self.BASEURL + 'currency=' + currency
        self.METHOD = 'GET'
        dict =  self.get_result()
        #print(dict)
        return dict['last']

    def getBalance(self, currency):
        self.URL = 'https://api.coinone.co.kr/v2/account/balance/'
        self.PAYLOAD = {}
        self.METHOD = 'POST'
        res = self.get_result()
        data = {}
        data['qtum'] = res[currency]['avail']
        data['krw'] = res['krw']['avail']
        # print(res[currency]['avail'], res['krw']['avail'])
        return data

    def evaluate(self, balance, coinPrice, currency):
        # 코인과 한화의 가치 평가
        krw = float(balance['krw'])
        coin = float(balance[currency]) * float(coinPrice)
        print('krw: ', krw, 'coin: ', coin)

        # 한화 가치가 더 높으면,
        even = (krw + coin)/2.0
        if(krw > coin):
            #coin을 krw - even 만큼 산다.
            print('한화가치 더 높음')
            self.limitBuy(currency, krw, coinPrice)
        else:
            #coin을 coin - even 만큼 판다.
            print('coin가치 더 높음')

    def limitBuy(self, currency, krw, coinPrice):
        self.URL = 'https://api.coinone.co.kr/v2/order/limit_buy/'
        self.METHOD = 'POST'
        payload = {
            "price": coinPrice,
            "qty": float(math.trunc((krw/coinPrice) * 10000) / 10000),  # 소수점 4자리수 까지
            "currency": currency
        }
        self.PAYLOAD = payload
        return self.get_result()

    def limitSell(self, currency, krw, coinPrice):
        self.URL = 'https://api.coinone.co.kr/v2/order/limit_sell/'
        self.METHOD = 'POST'
        payload = {
            "price": coinPrice,
            "qty": float(math.trunc((krw/coinPrice) * 10000) / 10000),  # 소수점 4자리수 까지
            "currency": currency
        }
        self.PAYLOAD = payload
        return self.get_result()


if __name__ == '__main__':
    ct = CoinOneTicker()
    ct.evaluate(ct.getBalance('qtum'), ct.getPrice('qtum'), 'qtum')
