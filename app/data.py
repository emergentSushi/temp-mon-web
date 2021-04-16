from app import app
from flask import render_template, jsonify
from datetime import timedelta, datetime
from flask_cors import cross_origin
from dateutil import tz

import sqlite3

nzst = tz.gettz('Pacific/Auckland')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
@cross_origin()
def devices():
	return jsonify({
		"A4:C1:38:3B:86:DE": { "title": "Bedroom", "colour": 'rgb(255, 99, 132)' },
		"A4:C1:38:73:28:DC": { "title": "Office", "colour": 'rgb(255, 159, 64)' },
		"A4:C1:38:A4:86:79": { "title": "Roof", "colour": 'rgb(75, 192, 192)' },
		"A4:C1:38:56:5C:07": { "title": "Kitchen", "colour": 'rgb(54, 162, 235)' },
	})

@app.route('/data')
@cross_origin()
def data():
	con = sqlite3.connect('../data/grid_data.db')
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	
	from_query = datetime.utcnow().astimezone(nzst) - timedelta(hours=12)
	
	rows = cur.execute(f'SELECT * FROM data WHERE timestamp > "{from_query.isoformat()}" ORDER BY timestamp DESC')
	ret = [dict(ix) for ix in rows]
	
	con.close()
	return jsonify(ret)
