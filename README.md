# temp-mon-web
Simple Flask app built to display temperature sensor data from a collection of Xiaomi LYWSD03MMC flashed with firmware from https://github.com/atc1441/ATC_MiThermometer

`sensor_reader/bt.py` is invoked by a cron job, which stores temperature, humidity and battery data in sqlite.
`app.py` is the entry point for the flask app that renders the data in a Flask site.

## Installation

`crontab -e` to configure a suitable interval for invoking `sensor_reader/bt.py` (which writes data to the sqlite db)
`docker-compose up -d` to run the hosting container

## Example output

![Example output graph](https://github.com/emergentSushi/temp-mon-web/blob/main/output.png?raw=true)

sensor_reader/bluetooth_utils.py shamelessly copied from https://github.com/colin-guyon/py-bluetooth-utils/blob/master/bluetooth_utils.py
