from datetime import datetime
from sqlite3 import Connection, Cursor, Row, connect
from typing import Any

from config import SensorConfig, SensorReading

PATH_TO_SQLITE = "data/grid_data.db"


def _get_sqlite_reader() -> Cursor:
    con = _get_sqlite_connection()
    return con.cursor()


def _get_sqlite_connection() -> Connection:
    con = connect(PATH_TO_SQLITE)
    con.row_factory = Row
    return con


def get_sensor_data(since: datetime) -> list[dict[Any, Any]]:
    con = _get_sqlite_reader()
    rows = con.execute("SELECT * FROM data WHERE timestamp > ? ORDER BY timestamp DESC", (since.isoformat(),)).fetchall()
    ret = [dict(ix) for ix in rows]

    con.close()

    return ret


def write_sensor_data(reading: SensorReading):
    connection = _get_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'INSERT INTO data VALUES ({reading.temperature}, {reading.humidity}, "{reading.date_recorded.isoformat()}", "{reading.mac}", {reading.battery})'
    )
    connection.commit()
    connection.close()


def get_configured_sensors() -> dict[str, SensorConfig]:
    return {
        "A4:C1:38:3B:86:DE": SensorConfig(mac="A4:C1:38:3B:86:DE", name="Larder", graph_colour="rgb(255, 99, 132)"),
        "A4:C1:38:73:28:DC": SensorConfig(mac="A4:C1:38:73:28:DC", name="Office", graph_colour="rgb(255, 159, 64)"),
        "A4:C1:38:A4:86:79": SensorConfig(mac="A4:C1:38:A4:86:79", name="Roof", graph_colour="rgb(75, 192, 192)"),
        "A4:C1:38:56:5C:07": SensorConfig(mac="A4:C1:38:56:5C:07", name="Kitchen", graph_colour="rgb(54, 162, 235)"),
        "A4:C1:38:EE:06:4C": SensorConfig(mac="A4:C1:38:EE:06:4C", name="Outdoor", graph_colour="rgb(97, 255, 51)"),
    }
