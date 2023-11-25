import http.client, json, threading
import time
from utils.bloxflipwebsocket import BaseWebsocket
from utils.captcha import BaseSolver

# Your bloxflip JWT
# How to get:
# Go to bloxflip.com on PC
# Press ctrl + shift + i
# Go to application
# Go to Local storage, then go to _DO_NOT_SHARE_BLOXFLIP_TOKEN
# Copy the value and past it between the "" below
AUTH_TOKEN = ""
# YOUR API KEY MUST BE A KEY FROM CAPSOLVER.COM, YOU HAVE TO GET BALANCE AS WELL TO BE ABLE TO SOLVE.
# MORE SUPPORT SOON
API_KEY = ""


class HttpClientBase(http.client.HTTPSConnection):
    def __init__(self):
        super().__init__(host="api.bloxflip.com", port=443)
        self.base_headers = {
            "Referer": "https://bloxflip.com/",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/117.0.5938.108 Mobile/15E148 Safari/604.1"
        }

    def requester(self, url):
        self.request('GET', url, headers=self.base_headers)
        return json.loads(self.getresponse().read().decode())


# http client base
httpBase = HttpClientBase()
solver = BaseSolver(API_KEY)

class BloxflipRain:
    def __init__(self):
        self.webconnect = BaseWebsocket(AUTH_TOKEN)
        self.webconnect.run_base()
    def checkrain(self):
        while True:
            connection = httpBase.requester('/chat/history')
            if connection['rain']['active']:
                captcha = solver.solve()
                if "error" not in captcha:
                    print('Solved captcha: %s!' % captcha)
                    self.webconnect.join_rain_data(captcha)
                    break
                else:
                    print('An error has occured %s' % captcha)
            time.sleep(5)


if __name__ == "__main__":
    b = BloxflipRain()
    threading.Thread(target=b.checkrain).start()
