# -*- coding: utf-8 -*-


from datetime import datetime
import dateutil.parser
import itertools
import requests


from powerdata import PowerData

class ClientData:
    
    def __init__(self, client_id):
        self.client_id = client_id
        self.power_data = PowerData()
        self.is_coffee_ready = False
        self.coffee_making_time = None

    def debug_print(self):
        attrs = vars(self)
        print ', '.join("%s: %s" % item for item in attrs.items())

data = {}

def process_data(client_id, values_raw, start, end):
    
    global data

    if not client_id in data:
        client_data = ClientData(client_id)
        data[client_id] = client_data
    else:
        client_data = data[client_id]

    print("client_id:{}".format(client_id))

    values_str = values_raw.split(",")
    
    values = map(int, values_str)
    
    #print(values)
    
    start_time = dateutil.parser.parse(start)
    end_time = dateutil.parser.parse(end)
     
    if len(values) == 0:
        # should not happen
        print("No data!!")
        return
    
    time_interval = (end_time - start_time) / len(values)
        
    print("time_interval:{}".format(time_interval))
        
    timeval = start_time
    for (value, items) in itertools.groupby(values):
        #print(value, items)
        count = len(list(items))
        
        client_data.power_data.add(value, timeval, timeval + time_interval * count)
        timeval += time_interval * count

    check_notify(client_data)


def check_notify(client_data):
    
    print("check_notify()")

    if client_data.is_coffee_ready == True:
        if client_data.power_data.is_off() == True:
            client_data.is_coffee_ready = False
    elif client_data.power_data.is_ready() == True:
        print("Coffee is ready", client_data.__dict__)
        client_data.is_coffee_ready = True
        client_data.coffee_making_time = datetime.now()
        notify(client_data)

         
def notify(client_data):
    print("sending notification for client:{}".format(client_data.client_id))
    payload = { "token": "aVrpYcqBBfE2rWVk3wW5yM28gLK3CH", 
                "user": "gkKtGcAqXZPZ4Yyeii8ArW6jx9oRA9",
                "title": u"Kahvia",
                "message": u"Tuoretta kahvetta ({})".format(client_data.client_id[:4]) }
    r = requests.post("https://api.pushover.net/1/messages.json", data=payload)


