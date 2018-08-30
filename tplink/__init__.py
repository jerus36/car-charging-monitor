import requests
import uuid
import json


class TPLink:
    def __init__(self, endpoint: str = "https://wap.tplinkcloud.com/"):
        self.endpoint = endpoint
        self.terminal_id = str(uuid.uuid4())
        self._token = None

    def _do_post(self, payload, params: dict = {}):
        params['token'] = self._token

        rsp = requests.post(self.endpoint, params=params, json=payload)
        data = rsp.json()
        if rsp.status_code == 200 and 'result' in data:
            return data['result']
        else:
            raise Exception(rsp.text)

    def login(self, user, password):
        payload = {
            "method": "login",
            "params":
                {
                    "appType": "AWS_Lambda",
                    "cloudUserName": user,
                    "cloudPassword": password,
                    "terminalUUID": self.terminal_id
                }
        }
        rsp = self._do_post(payload)
        self._token = rsp['token']

    @property
    def device_list(self):
        rsp = self._do_post({"method": "getDeviceList"})
        return rsp['deviceList']

    def passthrough(self, device_id: str, command: dict):
        params = {
            'appName': 'AWS_Lambda',
            'termID': self.terminal_id,
            'appVer': '1.0.0',
            'ospf': 'Android+6.0.1',
            'netType': 'wifi',
            'locale': 'en_US',
            'token': self._token
        };
        return self._do_post({
            "method": "passthrough",
            "params": {
                "deviceId": device_id,
                "requestData": json.dumps(command)
            }
        })['responseData']
