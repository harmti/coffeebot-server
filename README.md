Coffeebot
=========
Ever wondered how to let your colleagues know that you just made a fresh pot of coffee? Or felt frushtrated after finding (again) the coffee machine empty. Or wondered how fresh the coffee is.

Do you have a standard drip coffee machine and Ubiquiti Networks mFi mPower laying around?

No problem! Connect the company’s coffee machine to net and get alerts to slack when someone makes a pot of coffee. Coffeebot supports also pushover.net, hipchat and influxdb as the notification channel.

Coffeebot uses Ubiquiti Networks mFi mPower device https://www.ubnt.com/mfi/mpower/. Coffeebot runs as an extra process on the mPower device. It does not interact with the normal mFi Controller process.

Tested only on mPower mini decice, server running on Ubuntu.

How does it work
----------------
coffeebot-agent runs on nPower device. It uploads power consumption data to coffeebot-server. Server analyses the data and sends "Fresh Coffee!" alerts to configured channels.

See coffeebot-agent/README.md for agent setup instructions.

Eatch client has an unique persistent client ID.

Server configuration
--------------------
Edit notify.yaml as needed, define bot credentials for Slack etc.

Verify message sending works (to "test" clients) by running `python test_sending.py`.

Run `python app.py` to testdrive the setup. This also logs the client IDs of the connected agents.

Installation
------------
Install supervisor, create file `/etc/supervisor/conf.d/coffeebot-server.conf`:

```
[program:coffeebot-server]
command=python app.py
directory=<installation path>
stopasgroup=true
username=<some non root user>
autostart=true
autorestart=true
stderr_logfile=/var/log/coffeebot-server.err.log
stdout_logfile=/var/log/coffeebot-server.out.log
```

Run `sudo service supervisor reload` to reload the settings.
