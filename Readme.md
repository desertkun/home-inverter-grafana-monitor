# MUST Inverter PV1800 Grafana Monitor

A home monitoring solution for your MUST (or other modus-compatible) home inverter.

How to use:

1. Prepare a raspberry PI 4
2. Connect a USB cable to the Must PV1800 Inverter USB port
3. Go root (`sudo su`)
4. Install docker & docker-compose on it
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   chmod +x get-docker.sh
   ./get-docker.sh
   pip3 install docker-compose
   ```
5. Clone this repo
   ```bash
   git clone https://github.com/desertkun/must-pv1800-grafana-monitor.git
   cd must-pv1800-grafana-monitor
   ```
6. Go into the repo folder and do `docker-compose up -d`
7. Give it 20m to install everything and boot
8. Open `http://<rasperry-ip>:3000` and login with `admin/admin`
9. You should be redirected to an empty list of dashboards. Click New -> Import
10. Select [this file](./home-dashboard.json)

<img src="dashboard.jpg">

# But I have different model

1. Figure out the MODBUS device ID of your model, and the BAUD rate.
2. Look up the datasheet for register IDS that correspond to voltages etc
   as specified in [this script](./must/must.py) (see offset 25200 + register ids)
3. Modify the script, deploy as usual.

# I want notifications when power goes out

1. Create a bot on Telegram using https://t.me/BotFather
2. Create a new group with only you and that bot
3. Copy [the group Id](https://stackoverflow.com/a/49852274)
4. Open http://<ip>:3000/alerting/notifications
5. Select telegram as type, fill in token and group id, save the contact point.
   Select Notification policies, Select Default, click Edit, change contact point to Telegram
6. Edit e.g. the Input AC Panel: click Alerts -> Create Alert
7. Change Threshold to BELOW 100.
8. Click SAVE on the Dashboard