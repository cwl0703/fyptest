import logging
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy.engine import Engine
from sqlalchemy import event
from .indexview import FABView
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")
	
app.run()


