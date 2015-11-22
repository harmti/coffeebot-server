# -*- coding: utf-8 -*-


class DataPoint:
    
    def __init__(self, value, start_time, end_time):
        self.value = value
        self.start_time = start_time
        self.end_time = end_time

    def debug_print(self):
        print("  value:{}, start_time:{}, end_time:{}".format(self.value, self.start_time, self.end_time))


class PowerData:
    
    def __init__(self):
        self.power_data = []

    def add(self, value, start_time, end_time):
        if len(self.power_data) > 0 and self.power_data[-1].value == value:
            # just add to the latest item
            self.power_data[-1].end_time = end_time
        else:
            datapoint = DataPoint(value, start_time, end_time)
            self.power_data.append(datapoint)

        self.debug_print()

    def debug_print(self):
        print("PowerData len:{}".format(len(self.power_data)))
        for pd in self.power_data:
            pd.debug_print()

