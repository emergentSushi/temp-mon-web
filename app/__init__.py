from flask import Flask

app = Flask(__name__)

from app import data

app.config.from_pyfile("config.py")
