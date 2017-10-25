Coffeebot
=========
Ever wondered how to let your colleagues know that you just made a fresh pot of coffee? Or feelt frushtrated after finding (again) the coffee machine empty. Or wondered how fresh the coffee is.

Do you have a standard drip coffee machine and Ubiquiti Networks mFi mPower laying around?

No problem! Connect the company’s coffee machine to net and get alerts to slack when someone makes a pot of coffee. Supports also pushover.net, hipchat and influxdb.

Coffeebot used Ubiquiti Networks mFi mPower product https://www.ubnt.com/mfi/mpower/. Tested only on mPower mini.

How does it work
----------------

coffee-agent runs on nPower device. It uploads power consumption data to coffee-server. Server analyses the data and sends "Fresh Coffee!" alerts to configured channels.

See coffee-agent/README.md for agent setup instructions.

Eatch client has a unique persistent client ID.


Server configuration
--------------------
Edit notify.yaml as needed, define bot credentials for Slack etc.

Run `python test_sending.py` to test sending messages from a client (agent) ID named "test".

Run `python app.py` to test the setup. This also logs the client ID of connected agents.


Installation
------------
Install supervisor, create file `/etc/supervisor/conf.d/coffee-server.conf`:

```
[program:coffee-server]
command=python app.py
directory=<installation path>
stopasgroup=true
username=<some non root user>
autostart=true
autorestart=true
stderr_logfile=/var/log/coffee-server.err.log
stdout_logfile=/var/log/coffee-server.out.log

Run `sudo service supervisor restart` to reload settings.
