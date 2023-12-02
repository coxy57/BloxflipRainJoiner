import http.client, json, threading
import time
from utils.bloxflipwebsocket import BaseWebsocket
from utils.captcha import BaseSolver
from colorama import Fore,init
import secrets

# TO INSTALL ALL MODULES
# Paste pip install -r requirements.txt into your comand prompt and presse enter.

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

#call init func
init()

class HttpClientBase(http.client.HTTPSConnection):
    def __init__(self):
        super().__init__(host="api.bloxflip.com", port=443)
        self.base_headers = {
            "Referer": "https://bloxflip.com/",
            "x-auth-token": AUTH_TOKEN,
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
        self.solved = False
    def checkrain(self):
        while True:
            connection = httpBase.requester('/chat/history')
            if connection['rain']['active'] and not self.solved:
                captcha = solver.solve()
                if "error" not in captcha:
                    print(Fore.GREEN + 'Successfully solved captcha!')
                    cache = secrets.token_hex(10)
                    cache_result = httpBase.requester(f'/user?cache={cache}')
                    self.webconnect.join_rain_data(captcha,cache)
                    print('Joined rain!')
                    self.solved = True
                else:
                    print('An error has occured %s' % captcha)
            elif not connection['rain']['active'] and self.solved:
                self.solved = False
            else:
                x = secrets.token_hex(10)
                pass
            time.sleep(5)


if __name__ == "__main__":
    print(Fore.RED + "Running coxy57's auto joiner!")
    b = BloxflipRain()
    threading.Thread(target=b.checkrain).start()
