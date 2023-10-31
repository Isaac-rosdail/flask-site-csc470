from flask import Flask
import re
from datetime import datetime
from flask import render_template

app = Flask(__name__)
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tickets/")
def tickets():
    return render_template("tickets.html")
@app.route("/submit_ticket/")
def submit_ticket():
    return render_template("submit_ticket.html")