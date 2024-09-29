from flask import Flask, url_for

app = Flask(__name__, static_url_path="/static")
app.add_url_rule("/favicon.ico", redirect_to=url_for("static", filename="favicon.ico"))
