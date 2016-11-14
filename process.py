# -*- coding: utf-8 -*-

from datetime import datetime
import dateutil.parser
import itertools
import types


from powerdata import PowerData
from notify import Notify


g_client_data = {}


class ClientData:
    def __init__(self, client_id):
        self.client_id = client_id
        self.power_data = PowerData()
        self.is_coffee_ready = False
        self.coffee_making_time = None

    def __repr__(self):
        return "{}(client_id:{}, power_data:{}, is_coffee_ready:{}, coffee_making_time:{})".format(
            self.__class__, self.client_id, self.power_data, 
            self.is_coffee_ready, self.coffee_making_time)

class ProcessData:
    def __init__(self):
        self.notify = Notify()

    def process_data(self, client_id, values_raw, start, end):

        global g_client_data
    
        if not client_id in g_client_data:
            client_data = ClientData(client_id)
            g_client_data[client_id] = client_data
        else:
            client_data = g_client_data[client_id]

        #print("client_id:{}".format(client_id))

        values_str = values_raw.split(",")
    
        values = map(int, values_str)
    
        #print("Values:", values)
    
        start_time = dateutil.parser.parse(start)
        end_time = dateutil.parser.parse(end)
     
        if len(values) == 0:
            # should not happen
            print("No data!!")
            return
    
        time_interval = (end_time - start_time) / len(values)
        
        #print("time_interval:{}".format(time_interval))
        
        timeval = start_time
        for (value, items) in itertools.groupby(values):
            #print("iterate value, items", value, items)
            count = len(list(items))

            client_data.power_data.add(value, timeval, timeval + time_interval * count)
            timeval += time_interval * count

        self.check_notify(client_data)

    def check_notify(self, client_data):
    
        #print("check_notify()")
        #print(repr(client_data))

        if client_data.is_coffee_ready == True:
            if client_data.power_data.is_off() == True:
                print("Coffee machine turned off")
                client_data.is_coffee_ready = False
        elif client_data.power_data.is_ready() == True:
            print("Coffee is ready")
            client_data.is_coffee_ready = True
            client_data.coffee_making_time = datetime.now()
            self.notify.notify(client_data.client_id)

         
