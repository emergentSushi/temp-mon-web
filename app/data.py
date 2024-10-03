from datetime import datetime
from sqlite3 import Cursor, Row, connect
from typing import Any

from app import config


def _get_sqlite_reader() -> Cursor:
    con = connect(config.PATH_TO_SQLITE)
    con.row_factory = Row
    return con.cursor()


def get_sensor_data(since: datetime) -> list[dict[Any, Any]]:
    con = _get_sqlite_reader()
    rows = con.execute("SELECT * FROM data WHERE timestamp > ? ORDER BY timestamp DESC", (since.isoformat(),)).fetchall()
    ret = [dict(ix) for ix in rows]

    con.close()

    return ret
