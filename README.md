# temp-mon-web
Simple Flask app built to display temperature sensor data

sensor_reader/bt.py is invoked by a cron job, which creates grid_data.db with sqlite, storing data from Xiami LYWSD03MMC flashed with firmware from https://github.com/atc1441/ATC_MiThermometer

app.py is the entry point for the flask app that presents the grid_data.db data in a website.

Uses the flask dev server for hosting, because it sits behind a nat, this probably isn't production ready ;)
