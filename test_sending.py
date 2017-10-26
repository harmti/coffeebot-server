#!/bin/python

from datetime import datetime

import notify
from clientdata import ClientData

def main():
    client = ClientData("test")
    client.coffee_making_duration = 222
    client.is_coffee_ready = True
    client.coffee_making_time = datetime.now()

    notifier = notify.Notify()
    notifier.notify(client)

if __name__ == "__main__":
    main()
