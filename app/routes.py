from app import app
from flask import render_template, jsonify
from datetime import timedelta, datetime
from flask_cors import cross_origin

import sqlite3

devices_data = {
	"A4:C1:38:3B:86:DE": "Loose",
	"A4:C1:38:73:28:DC": "Mathew Office",
	"A4:C1:38:A4:86:79": "Roof",
	"A4:C1:38:56:5C:07": "Kitchen",
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
def devices():
	return jsonify(devices_data)

@app.route('/data')
@cross_origin()
def data():
	con = sqlite3.connect('grid_data.db')
	cur = con.cursor()

	from_query = datetime.now() - timedelta(hours=1)
	
	ret = []
	for row in cur.execute(f'SELECT * FROM data WHERE timestamp > "{from_query.isoformat()}" ORDER BY timestamp DESC'):
		ret.append(row)
	con.close()
	return jsonify(ret)
