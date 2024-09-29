import sqlite3
from datetime import datetime, timedelta, timezone

from dateutil import tz
from flask import Response, jsonify, render_template
from flask.wrappers import Request
from flask_cors import cross_origin

from app import app

nzst = tz.gettz("Pacific/Auckland")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/devices")
@cross_origin()
def devices() -> Response:
    return jsonify(
        {
            "A4:C1:38:3B:86:DE": {"title": "Larder", "colour": "rgb(255, 99, 132)"},
            "A4:C1:38:73:28:DC": {"title": "Office", "colour": "rgb(255, 159, 64)"},
            "A4:C1:38:A4:86:79": {"title": "Roof", "colour": "rgb(75, 192, 192)"},
            "A4:C1:38:56:5C:07": {"title": "Kitchen", "colour": "rgb(54, 162, 235)"},
            "A4:C1:38:EE:06:4C": {"title": "Outdoor", "colour": "rgb(97, 255, 51)"},
        }
    )


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
