#!/usr/bin/env python3
import sys
import time
from datetime import datetime
import sqlite3
import bluetooth._bluetooth as bluez

from bluetooth_utils import (toggle_device, enable_le_scan,
                             parse_le_advertising_events,
                             disable_le_scan, raw_packet_to_str)

devices = {
    "A4:C1:38:3B:86:DE": "Loose",
    "A4:C1:38:73:28:DC": "Mathew Office",
    "A4:C1:38:A4:86:79": "Roof",
    "A4:C1:38:56:5C:07": "Kitchen",
}

scan_count = 0

def store(con, data_str, mac):
    global scan_count
    temp = int(data_str[22:26], 16) / 10
    humidity = int(data_str[26:28], 16)
    battery = int(data_str[28:30], 16)
    print("%s - Device: %s Temp: %sc Humidity: %s%% Batt: %s%%" % (datetime.now().isoformat(), devices[mac], temp, humidity, battery))

    cur = con.cursor()
    cur.execute(f'INSERT INTO data VALUES ({temp}, {humidity}, "{datetime.now().isoformat()}", "{mac}", {battery})')
    con.commit()
    scan_count += 1

    if scan_count == len(devices):
        sys.exit()

def db_init():
    global scan_count

    con = sqlite3.connect('/home/pi/data/grid_data.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS data (temp REAL, humidity REAL, timestamp varchar(24), mac varchar(17), battery int)')
    cur.execute('CREATE INDEX IF NOT EXISTS datetime_index ON data(timestamp)')
    con.commit()
    
    return con



con = db_init()
dev_id = 0 # Use 0 for hci0
toggle_device(dev_id, True)
 
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise
 
enable_le_scan(sock, filter_duplicates=False)



try:

    def le_advertise_packet_handler(mac, adv_type, data, rssi):
        data_str = raw_packet_to_str(data)
        if data_str[6:10] == '1a18' and mac in devices:
            store(con, data_str, mac)

    parse_le_advertising_events(sock,
                                handler=le_advertise_packet_handler,
                                debug=False)
# allow keyboard kill
except KeyboardInterrupt:
    disable_le_scan(sock)
