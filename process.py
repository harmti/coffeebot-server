# -*- coding: utf-8 -*-


from datetime import datetime
import dateutil.parser
import itertools

from powerdata import PowerData

pd = PowerData()

def process_data(values_raw, start, end):
    
    global pd

    values_str = values_raw.split(",")
    
    values = map(int, values_str)
    
    print(values)
    
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
        print(value, items)
        count = len(list(items))
        
        pd.add(value, timeval, timeval + time_interval * count)
        timeval += time_interval * count
         
         
def notify():
    payload = { "token": "aVrpYcqBBfE2rWVk3wW5yM28gLK3CH", 
                "user": "gkKtGcAqXZPZ4Yyeii8ArW6jx9oRA9",
                "title": u"Kahvia",
                "message": u"Tuoretta kahvetta nelosen keittiössä" }
    r = requests.post("https://api.pushover.net/1/messages.json", data=payload)


