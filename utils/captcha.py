import requests

class BaseSolver:
    def __init__(self,api_key: str):
        self.api_key = api_key
        self.base_headers = {
            'Host': 'api.capsolver.com',
            'Content-Type': 'application/json'
        }
    def solve(self):
        create_cap = requests.post('https://api.capsolver.com/createTask',json={
            "clientKey": self.api_key,
            "task": {
                "type": "HCaptchaTaskProxyLess",
                "websiteURL": "https://bloxflip.com/",
                "websiteKey": "2ce02d80-0c81-4b28-8af5-e4cdfc08bed9",
            }
        },headers=self.base_headers)
        if "taskId" in create_cap.text:
            taskid = create_cap.json()['taskId']
            while True:
                r = requests.post('https://api.capsolver.com/getTaskResult',json={
                    'clientKey': self.api_key,
                    'taskId': taskid
                },headers=self.base_headers)
                if "solution" in r.text:
                   return r.json()['solution']['gRecaptchaResponse']
        else:
            return "error: %s" % create_cap.text
