import logging
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy.engine import Engine
from sqlalchemy import event
from .indexview import FABView
from flask import render_template

app = Flask(__name__)


users = [{"username": "我", "url": "我-APP-的名字.herokuapp.com"},
         {"username": "你", "url": "你-APP-的名字.herokuapp.com"}]

@app.route("/")
def home():
    return render_template("base.html",users=users)

app.run()
