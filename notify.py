import json
import requests

import yaml
from yaml import load, dump
from yaml import Loader, Dumper

# ...

CONF_FILE="notify.yaml"


class Notify:

    def __init__(self):
        self.config = self.read_config()

    def read_config(self):
        with open(CONF_FILE, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def notify(self, client):
        print("sending notification for client:'{}'".format(client))
        for sender, protodata in self.config['senders'].items():
            if client in protodata['clients']:
                getattr(self, protodata['protocol'])(client, protodata)
        #self.pushover_notify(client)
        #self.hipchat_notify(client)

    def pushover(self, client, data):
        payload = { "token": data['token'], 
                    "user": data['user'],
                    "title": data['title'],
                    "message": data['message'] }
        r = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        print(r.text)
    

    def hipchat(self, client, data):
        # API V2, send message to room:
        url = 'https://{}/v2/room/{}/notification'.format(data['server'], data['roomid'])
        message = data['message']
        headers = {
            "content-type": "application/json",
            "authorization": "Bearer {}".format(data['token'])}
        datastr = json.dumps({
            'message': message,
            'color': data['color'],
            'message_format': 'html',
            'notify': True})
        r = requests.post(url, headers=headers, data=datastr)
        print(r.text)

    


