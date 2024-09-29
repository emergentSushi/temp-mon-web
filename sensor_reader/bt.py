#!/usr/bin/env python3
import sqlite3
import sys
import threading
from datetime import datetime

from bluetooth_utils import (
    disable_le_scan,
    enable_le_scan,
    get_sock,
    parse_le_advertising_events,
    raw_packet_to_str,
    toggle_device,
)

devices = {
    "A4:C1:38:3B:86:DE": "Larder",
    "A4:C1:38:73:28:DC": "Mathew Office",
    "A4:C1:38:A4:86:79": "Roof",
    "A4:C1:38:56:5C:07": "Kitchen",
    "A4:C1:38:EE:06:4C": "Outdoor",
}

readings = {}


def store(con, data_str, mac) -> None:
    temp = int(data_str[22:26], 16) / 10
    humidity = int(data_str[26:28], 16)
    battery = int(data_str[28:30], 16)
    print(
        "%s - Device: %s Temp: %sc Humidity: %s%% Batt: %s%%"
        % (datetime.now().isoformat(), devices[mac], temp, humidity, battery)
    )

    cur = con.cursor()
    cur.execute(
        f'INSERT INTO data VALUES ({temp}, {humidity}, "{datetime.now().isoformat()}", "{mac}", {battery})'
    )
    con.commit()

    readings[mac] = {"temp": temp, "humidity": humidity, "battery": battery}
    if len(readings) == len(devices):
        self_destruct()


def db_init() -> sqlite3.Connection:
    con = sqlite3.connect("/home/pi/data/grid_data.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS data (temp REAL, humidity REAL, timestamp varchar(24), mac varchar(17), battery int)"
    )
    cur.execute("CREATE INDEX IF NOT EXISTS datetime_index ON data(timestamp)")
    con.commit()

    return con


con = db_init()
toggle_device(0, True)

try:
    sock = get_sock()
except:
    print("Cannot open bluetooth device")
    raise

enable_le_scan(sock, filter_duplicates=True)


def self_destruct() -> None:
    disable_le_scan(sock)
    sys.exit()


try:

    def le_advertise_packet_handler(mac, adv_type, data, rssi):
        data_str = raw_packet_to_str(data)
        if data_str[6:10] == "1a18" and mac in devices:
            store(con, data_str, mac)

    threading.Timer(30, self_destruct).start()

    parse_le_advertising_events(sock, handler=le_advertise_packet_handler, debug=False)
except KeyboardInterrupt:
    self_destruct()
