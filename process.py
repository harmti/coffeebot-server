# -*- coding: utf-8 -*-

from datetime import datetime
import dateutil.parser
import itertools

from notify import Notify
from clientdata import ClientData

g_client_data = {}

class ProcessData(object):
    def __init__(self):
        self.notify = Notify()

    def process_data(self, data):

        global g_client_data

        if data['client_id'] not in g_client_data:
            client_data = ClientData(data['client_id'])
            g_client_data[data['client_id']] = client_data
        else:
            client_data = g_client_data[data['client_id']]

        values = list(map(int, data['values'].split(",")))
        start_time = dateutil.parser.parse(data['start_time'])
        end_time = dateutil.parser.parse(data['end_time'])

        if len(data['values']) == 0:
            # Client did not senD any ata. This should not happen, but just ignore.
            print("Client did not send any data!!")
            return

        # Duration of one measurement value. This assumes client uses fixed
        # slot duration.
        slot_duration = (end_time - start_time) / len(values)

        timeval = start_time
        for (value, items) in itertools.groupby(values):
            count = len(list(items))

            client_data.power_data.add(value, timeval, timeval + slot_duration * count)
            timeval += slot_duration * count

        self.check_notify(client_data)

    def check_notify(self, client_data):

        (is_fresh_coffee, making_duration) = client_data.power_data.is_ready()

        if client_data.is_coffee_ready is True:
            if client_data.power_data.is_off() is True:
                print("Coffee machine turned off")
                client_data.is_coffee_ready = False
        elif is_fresh_coffee is True:
            print("Coffee is ready")
            client_data.is_coffee_ready = True
            client_data.coffee_making_time = datetime.now()
            client_data.coffee_making_duration = making_duration
            self.notify.notify(client_data)
