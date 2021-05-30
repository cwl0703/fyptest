import logging
from flask import Flask , render_template , request, send_file
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy.engine import Engine
from sqlalchemy import event
from .indexview import FABView
from .models import Item
from datetime import datetime
from sqlalchemy import cast, Date


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
valueList={"rr"}
app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
valueList = {"rr","bb"}
appbuilder = AppBuilder(app, db.session , base_template='mybase.html',indexview=FABView ) #

"""
Only include this for SQLLite constraints
"""
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    

from app import views, data

#MAIN PAGE
# processor is for main page to load latest product.
# processor is loaded before loading template.
#1.Call Model to get data
#2.use Contetxt_processor pass value to MainPage, must use dict(key=value) e.g. dict(result=database_data)
@app.context_processor
def process():
    return dict(uesr_result=({"url":"www.yahoo.com.hk","image": "img/camera.png","name":"Camera"},
                             {"url":"www.yahoo.com.hk","image": "img/ear_phone.jpg","name":"Ear Phone"}))


#SEARCH PAGE
@app.route("/search", methods=['GET','POST'])
def searchView():
    if request.method == "POST":
        result = request.form
        #search Model by result key
        return render_template("search/search_result.html",base_template='mybase.html', appbuilder=appbuilder, result=result)
    else:
        return render_template("search/search.html",base_template='mybase.html', appbuilder=appbuilder)

@app.route("/")
def home():
    return "Welcome to the HomePage!"



######### Calvin  ##########
#########   API   ##########
# Display Object
# 1.Banner, 2.Daily Product, 3.Product Detail, 4.Profile
##############
#1. GET BANNER 
##############
@app.route("/getBannerImage/<image_name>", methods=['GET'])
def getBannerImage(image_name):
    filename = "static/img/" + image_name
    return send_file(filename, mimetype=image_name.split(".")[1])
#############
#2. Daily Product
#############
@app.route("/getDailyProduct", methods=['GET'])
def getDailyProduct():
    #db.session.query(YourModelName).query.limit(10).all()ser.query.filter_by(username='missing').first()
    return db.session.query(Item.cast(Date)).distinct().all()


#
#3. 
#4.


#data.fill_gender()
#data.fill_data()
    
db.create_all()