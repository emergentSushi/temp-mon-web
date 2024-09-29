import sqlite3
from datetime import datetime, timedelta, timezone

from dateutil import tz
from flask import Response, jsonify, render_template
from flask.wrappers import Request
from flask_cors import cross_origin

from app import app
from app.config import sensors

nzst = tz.gettz("Pacific/Auckland")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/devices")
@cross_origin()
def devices() -> Response:
    return jsonify(sensors)


@app.route("/data")
@cross_origin()
def data() -> Response | tuple[Response, int]:
    try:
        startDate = datetime.now(timezone.utc)

        startDateArg = Request.args.get("start")
        if startDateArg is not None:
            startDate = datetime.utcfromtimestamp(int(startDateArg))

        hoursBack = 12
        hoursBackArg = Request.args.get("hours")
        if hoursBackArg is not None:
            hoursBack = int(hoursBackArg)

        from_query = startDate.astimezone(nzst) - timedelta(hours=hoursBack)

        con = sqlite3.connect(app.config["PATH_TO_SQLITE"])
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        rows = cur.execute(f'SELECT * FROM data WHERE timestamp > "{from_query.isoformat()}" ORDER BY timestamp DESC')
        ret = [dict(ix) for ix in rows]

        con.close()
        return jsonify(ret)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
