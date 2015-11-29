# -*- coding: utf-8 -*-

POWER_OFF, POWER_WARMUP, POWER_MAKING = range(3)

MIN_MAKING_TIME_S = 60

def power_state(value):
    if value < 2:
        return POWER_OFF
    if value < 500:
        return POWER_WARMUP
    else:
        return POWER_MAKING


class DataPoint:
    
    def __init__(self, value, start_time, end_time):
        self.power_state = power_state(value)
        self.start_time = start_time
        self.end_time = end_time

    def debug_print(self):
        print("  power_state:{}, start_time:{}, end_time:{}".format(
            self.power_state, self.start_time, self.end_time))

                

class PowerData:
    
    def __init__(self):
        self.power_data = []

    def add(self, value, start_time, end_time):
        if len(self.power_data) > 0 and self.power_data[-1].power_state == power_state(value):
            # just add to the latest item
            self.power_data[-1].end_time = end_time
        else:
            datapoint = DataPoint(value, start_time, end_time)
            self.power_data.append(datapoint)

        self.debug_print()

    def check_if_trigger(self):
        if len(self.power_data) <= 2:
            return False

        if self.power_data[-1].power_state != POWER_WARMUP:
            return False

        if self.power_data[-2].power_state != POWER_MAKING:
            return False

        diff = self.power_data[-2].end_time - self.power_data[-2].start_time

        if diff.seconds < MIN_MAKING_TIME_S:
            return False

        return True
                    


    def debug_print(self):
        print("PowerData len:{}".format(len(self.power_data)))
        for pd in self.power_data:
            pd.debug_print()

