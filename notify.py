import json
import requests

import yaml
from yaml import load, dump
from yaml import Loader, Dumper

from clientdata import ClientData


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
        for sender, conf in self.config['senders'].items():
            if ('*' in conf['clients'] and client.client_id != "test") or client.client_id in conf['clients']:
                getattr(self, conf['protocol'])(client, conf)

    def pushover(self, client, conf):
        payload = { "token": conf['token'],
                    "user": conf['user'],
                    "title": conf['title'],
                    "message": conf['message'] }
        r = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        self.report_success(r)

    def hipchat(self, client, conf):
        # API V2, send message to room:
        url = 'https://{}/v2/room/{}/notification'.format(conf['server'], conf['roomid'])
        headers = {
            "content-type": "application/json",
            "authorization": "Bearer {}".format(conf['token'])}
        datastr = json.dumps({
            'message': conf['message'],
            'color': conf['color'],
            'message_format': 'html',
            'notify': True})
        r = requests.post(url, headers=headers, data=datastr)
        self.report_success(r)

    def slack(self, client, conf):
        url = 'https://hooks.slack.com/services/{}'.format(conf['token'])
        headers = {"content-type": "application/json"}
        datastr = json.dumps({
            'channel': conf['channel'],
            "attachments":[{
                'title': conf['message'],
                'color': conf['color']
                }]
        })
        print(datastr)
        r = requests.post(url, headers=headers, data=datastr)
        self.report_success(r)

    def influxdb(self, client, conf):
        url = 'http://' + conf['server'] + ":" + str(conf['port']) + '/write'
        headers = {"content-type": "application/octet-stream"}
        auth = (conf['user'], conf['password'])
        params = { 'db': conf['database'] }
        payload = conf['measurement']
        payload += ",machine=" + conf['machine'] + ",id=" + client.client_id
        payload += " {}={}".format('duration_s', client.coffee_making_duration)
        print(url, headers, auth, params, payload)
        r = requests.post(url, headers=headers, auth=auth, params=params, data=payload)
        self.report_success(r)


