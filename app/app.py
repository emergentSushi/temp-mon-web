from datetime import datetime, timedelta

from flask import Flask, Response, jsonify, render_template, request
from flask_cors import cross_origin

from app.config import sensors
from app.data import get_sensor_data

app = Flask(__name__, static_url_path="/static")

DEFAULT_HOURS = 18


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/devices")
@cross_origin()
def devices() -> Response:
    return jsonify({key: value.model_dump() for key, value in sensors.items()})


@app.route("/data")
@cross_origin()
def data() -> Response | tuple[Response, int]:
    try:
        startDate = datetime.now()
        startDateArg = request.args.get("start")
        if startDateArg is not None:
            startDate = datetime.fromtimestamp(int(startDateArg))

        hoursBack = DEFAULT_HOURS
        hoursBackArg = request.args.get("hours")
        if hoursBackArg is not None:
            hoursBack = int(hoursBackArg)

        from_query = startDate - timedelta(hours=hoursBack)
        ret = get_sensor_data(from_query)

        return jsonify(ret)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
