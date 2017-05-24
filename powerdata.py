# -*- coding: utf-8 -*-

POWER_OFF, POWER_WARMUP, POWER_MAKING = range(3)

# coffee machine has to be on at least this many seconds
MIN_MAKING_TIME_S = 60

# don't anymore report if this many seconds has already passed
MAX_WARMUP_TIME_FOR_NOTIFY_S = 10 * 60

# data is stored in memory for this time
STORE_DATA_TIME_S = 60 * 60


def power_state(value):
    if value < 2:
        return POWER_OFF
    if value < 300:
        return POWER_WARMUP
    else:
        return POWER_MAKING


class DataPoint:
    
    def __init__(self, value, start_time, end_time):
        self.power_state = power_state(value)
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return "{}(power_state:{}, start_time:{}, end_time:{})".format(
            self.__class__, self.power_state, self.start_time, self.end_time)
                

class PowerData:
    
    def __init__(self):
        self.power_data = []

    def __repr__(self):
        ret = "{}(len:{}, {})".format(self.__class__, len(self.power_data), self.power_data)
        
        return ret

    def add(self, value, start_time, end_time):
        #print("PowerData.add: before", self)
        if len(self.power_data) > 0 and self.power_data[-1].power_state == power_state(value):
            # just add to the latest item
            self.power_data[-1].end_time = end_time
        else:
            datapoint = DataPoint(value, start_time, end_time)
            self.power_data.append(datapoint)

        # delete 'old' data
        if len(self.power_data) > 10:
            diff_time = self.power_data[-1].end_time - self.power_data[0].start_time
            if diff_time.seconds > STORE_DATA_TIME_S:
                del self.power_data[0]

        #print("PowerData.add: after", self)

    def is_off(self):
        if len(self.power_data) <= 1:
            return True

        if self.power_data[-1].power_state != POWER_OFF:
            return False

        return True


    def is_ready(self):
        if len(self.power_data) <= 2:
            return (False, 0)

        if self.power_data[-1].power_state != POWER_WARMUP:
            return (False, 0)

        if self.power_data[-2].power_state != POWER_MAKING:
            return (False, 0)

        making_time = self.power_data[-2].end_time - self.power_data[-2].start_time
        warmup_time = self.power_data[-1].end_time - self.power_data[-1].start_time

        if making_time.seconds < MIN_MAKING_TIME_S:
            return (False, 0)

        # Don't bother to report if this is already old news.  This
        # should not happen in normal scenrarious, as client reports
        # the power usage rather quickly. Anyway can happen in error
        # situations, like network or server hickups.
        if warmup_time.seconds > MAX_WARMUP_TIME_FOR_NOTIFY_S:
            return (False, 0)

        return (True, making_time.seconds)
