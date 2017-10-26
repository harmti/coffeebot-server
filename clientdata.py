
from powerdata import PowerData

class ClientData(object):
    def __init__(self, client_id):
        self.client_id = client_id
        self.power_data = PowerData()
        self.is_coffee_ready = False
        self.coffee_making_time = None
        self.coffee_making_duration = 0

    def __repr__(self):
        return "{}(client_id:{}, power_data:{}, is_coffee_ready:{}, coffee_making_time:{}, coffee_making_duration:{})".format(
            self.__class__, self.client_id, self.power_data,
            self.is_coffee_ready, self.coffee_making_time, self.coffee_making_duration)

