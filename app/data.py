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

@app.route('../data')
@cross_origin()
def data():
	con = sqlite3.connect('data/grid_data.db')
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	
	from_query = datetime.now().astimezone(nzst) - timedelta(hours=12)
	
	rows = cur.execute(f'SELECT * FROM data WHERE timestamp > "{from_query.isoformat()}" ORDER BY timestamp DESC')
	ret = [dict(ix) for ix in rows]
	
	con.close()
	return jsonify(ret)
