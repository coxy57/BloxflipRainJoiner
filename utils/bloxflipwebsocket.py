import websocket, time, threading


class BaseWebsocket(websocket.WebSocketApp):
    def init(self,auth):
        self.auth = auth
        self.base_headers = {
            'Origin': 'https://bloxflip.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
        super().init(url="wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket", header=self.base_headers,
                         on_message=lambda ws, msg: self.client_recv(ws, msg), on_open=lambda ws: self.open(ws),
                         on_close=lambda ws, close_status_code, close_msg: self.on_close(ws, close_status_code,
                                                                                         close_msg))

    def client_recv(self, ws, msg):
        if msg.strip() == "3":
            print('Server is being pinged!')
            ws.send('2')
        else:
           pass
    def join_rain_data(self, token,cache):
        try:
            self.send(f'42/chat,["enter-rain",{{"captchaToken":"{token};;{cache};;scope"}}]')
        except Exception as e:
            self.send(f'42/chat,["enter-rain",{{"captchaToken":"{token};;{cache};;scope"}}]')
    def open(self, ws):
        ws.send('40/chat,')
        time.sleep(0.2)
        ws.send(f'42/chat,["auth","{self.auth}"]')
    def on_close(self, ws, status_code, close_msg):
        print(close_msg, status_code)

    def run_base(self):
        threading.Thread(target=self.run_forever).start()
