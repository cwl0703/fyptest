import logging
import os
from flask import Flask, request
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy.engine import Engine
from sqlalchemy import event
from .indexview import FABView
from flask import render_template


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLA(app)
db.init_app(app)

def web_select_specific(condition):  
	condition_query = []
	
	for key, value in condition.items():
		if value:
			condition_query.append(f"{key}='{value}'")
	if condition_query:
		condition_query = "WHERE " + ' AND '.join(condition_query)
	else:
		condition_query = ''
	
	postgres_select_query = f"""SELECT * FROM ab_register_user {condition_query} ORDER BY id;"""
	print(postgres_select_query)
	
	table = []
	table.extend(db.engine.execute(postgres_select_query).fetchall())

	return table


optionsList = [["想食野","eat_what"],["想睇電視","look_look"],["咩都唔想做","do_nothing"],["測試成功","test_success"]]

@app.route("/")
def create_dropList():
	return render_template("drop_list_form.html",options=optionsList)
	
app.run()


