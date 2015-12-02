# -*- coding: utf-8 -*-

POWER_OFF, POWER_WARMUP, POWER_MAKING = range(3)

# coffee machine has to be on at least this many seconds
MIN_MAKING_TIME_S = 60

# don't anymore report if this many seconds has already passed
MAX_WARMUP_TIME_FOR_NOTIFY_S = 10 * 60

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

        #self.debug_print()

    def is_off(self):
        if len(self.power_data) <= 1:
            return True

        if self.power_data[-1].power_state != POWER_OFF:
            return False

        return True


    def is_ready(self):
        if len(self.power_data) <= 2:
            return False

        if self.power_data[-1].power_state != POWER_WARMUP:
            return False

        if self.power_data[-2].power_state != POWER_MAKING:
            return False

        making_time = self.power_data[-2].end_time - self.power_data[-2].start_time
        warmup_time = self.power_data[-1].end_time - self.power_data[-1].start_time

        if making_time.seconds < MIN_MAKING_TIME_S:
            return False

        # Don't bother to report if this is already old news.  This
        # should not happen in normal scenrarious, as client reports
        # the power usage rather quickly. Anyway can happen in error
        # situations, like network or server hickups.
        if warmup_time.seconds > MAX_WARMUP_TIME_FOR_NOTIFY_S:
            return False

        return True
                    


    def debug_print(self):
        print("PowerData len:{}".format(len(self.power_data)))
        for pd in self.power_data:
            pd.debug_print()

