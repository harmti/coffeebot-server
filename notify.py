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

    def report_success(self, response):
        print("{} {}".format(response.status_code, response.text))

    def notify(self, client):
        print("sending notification for client:'{}'".format(client))
        for sender, protodata in self.config['senders'].items():
            if '*' in protodata['clients'] or client in protodata['clients']:
                getattr(self, protodata['protocol'])(client, protodata)

    def pushover(self, client, data):
        payload = { "token": data['token'], 
                    "user": data['user'],
                    "title": data['title'],
                    "message": data['message'] }
        r = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        self.report_success(r)

    def hipchat(self, client, data):
        # API V2, send message to room:
        url = 'https://{}/v2/room/{}/notification'.format(data['server'], data['roomid'])
        headers = {
            "content-type": "application/json",
            "authorization": "Bearer {}".format(data['token'])}
        datastr = json.dumps({
            'message': data['message'],
            'color': data['color'],
            'message_format': 'html',
            'notify': True})
        r = requests.post(url, headers=headers, data=datastr)
        self.report_success(r)

    def slack(self, client, data):
        url = 'https://hooks.slack.com/services/{}'.format(data['token'])
        headers = {"content-type": "application/json"}
        datastr = json.dumps({
            'channel': data['channel'],
            "attachments":[{
                'title': data['message'],
                'color': data['color']
                }]
        })
        print(datastr)
        r = requests.post(url, headers=headers, data=datastr)
        self.report_success(r)


