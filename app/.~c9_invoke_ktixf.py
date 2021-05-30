import logging, re
from flask import Flask , render_template , request, send_file,jsonify , redirect
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy.engine import Engine
from sqlalchemy import event , desc , asc
from .indexview import FABView
from .models import Item , Category
from .aws_api import amazonApi 
import datetime
import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.security.registerviews import RegisterUserDBView
from flask_babel import lazy_gettext

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
valueList={"rr"}
app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
valueList = {"rr","bb"}
appbuilder = AppBuilder(app, db.session , base_template='mybase.html',indexview=FABView )
aws = amazonApi()
app.url_map.strict_slashes = False

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
    return dict(itemlists=db.session.query(Item).order_by(desc(Item.viewCounter)).limit(10),
                itemlists2=db.session.query(Item).order_by(desc(Item.createdDate)).limit(10))
                         
@app.context_processor                             
def category_list():
    print("-----------------------")
    
    return dict(category_list=db.session.query(Category).filter_by(parentCategoryID="").all())


#SEARCH PAGE
@app.route("/search", methods=['GET','POST'])
def searchView():
    if request.method == "POST":
        result = request.form
        #search Model by result key
        return render_template("search/search_result.html",base_template='mybase.html', appbuilder=appbuilder, result=result)
    else:
        return render_template("search/search.html",base_template='mybase.html', appbuilder=appbuilder)

#Product Detail
@app.route("/product_detail/itemId=<itemId>")
def getProductDetails(itemId):
    #database
    item = db.session.query(Item).filter_by(id=itemId).first()
    category = db.session.query(Category).filter_by(id=item.categoryID).first()
    if category.parentCategoryID!="":
        parentCategory = db.session.query(Category).filter_by(id=category.parentCategoryID).first()
    else:
        parentCategory=""
    viewCounter(item.id)
    return render_template("product/product.html",base_template='mybase.html',
                            appbuilder=appbuilder, item=item,category=category , parentCategory=parentCategory)
    
# Product List
@app.route('/product_list/categoryId=<int:categoryId>')
@app.route('/product_list/productId=<int:productId>')  #<------------------for what? 
def getProductListByCategoryId(categoryId=None,productId=None):
    product_list=find_ProductList(categoryId)[0]
    lists=find_ProductList(categoryId)[1]
    lists2=[]
    for list in lists :
        lists2.append(db.session.query(Category).filter_by(id=list).first().categoryName)
    lists = dict(zip(lists,lists2))
    return  render_template("product/product_list.html",base_template='mybase.html', appbuilder=appbuilder,product_list=product_list,lists=lists)

def find_ProductList(catId):
    cat = db.session.query(Category).filter_by(id=catId).first()
    lists=[cat.id]
    if cat.parentCategoryID is not None:
        catList = []
        subCatList = db.session.query(Category).filter_by(parentCategoryID=cat.id).all()
        for cats in subCatList:
             lists.append(cats.id)
        for list in lists:
            catList.extend(db.session.query(Item).filter_by(categoryID=list).all())
    else:
        catList = db.session.query(Item).filter_by(categoryID=catId).all()
    return catList ,lists

# Most-Recent Page
@app.route('/product_list/recent')
def getProductListByTime():
    product_list=db.session.query(Item).order_by(desc(Item.createdDate)).all()
    title="Most Recent"
    return  render_template("product/product_list.html",base_template='mybase.html', appbuilder=appbuilder,product_list=product_list,title=title)

# Most-Popular Page
@app.route('/product_list/popular')
def getProductListByView():
    product_list=db.session.query(Item).order_by(desc(Item.viewCounter)).all()
    title="Most Popular"
    return  render_template("product/product_list.html",base_template='mybase.html', appbuilder=appbuilder,product_list=product_list,title=title)

#Redirect to User-Register Page
@app.route('/register')
def userRegister():
      return redirect("register/form")
    
#UserProduct CRUD Page

#Function for View Counter
def viewCounter(itemId):
    item = db.session.query(Item).filter_by(id=itemId).first()
    item.viewCounter +=1
    db.session.commit()


#########   API   ##########
# Display Object
# 1.Banner, 2.Daily Product, 3.Product Detail, 4.Profile 5.userLogin 6.AWS send SMS
##############
#1. GET BANNER 
##############
@app.route("/getBannerImage?imageName=<image_name>", methods=['GET'])
def getBannerImage(image_name):
    filename = "static/img/" + image_name
    return send_file(filename, mimetype=image_name.split(".")[1])
#############
#2. Daily Product
#############
@app.route("/getDailyProduct", methods=['GET'])
def getDailyProduct():
    return jsonify(json_list= db.session.query(Item.itemName, Item.price, Item.itemDescription).all())
#############
#3. Product Detail
#############
@app.route("/getProductDetail?itemId=<itemId>", methods=['GET'])
def getProductDetailById(itemId):
    return jsonify(db.session.query(Item.id, Item.id, Item.categoryID,Item.itemName, Item.price, Item.itemDescription, Item.itemStatusID, Item.viewCounter).filter(Item.id==itemId).first())
@app.route("/getProductDetail?itemName=<itemName>", methods=['GET'])
def getProductDetailByName(itemName):
    return jsonify(db.session.query(Item.id, Item.id, Item.categoryID,Item.itemName, Item.price, Item.itemDescription, Item.itemStatusID, Item.viewCounter).filter(Item.itemName==itemName).first())
#############
#4. Profile
#############
  
@app.route("/getUser?username=<username>", methods=['GET'])
def getUser(username):
    return jsonify(db.session.query(User.id, User.email, User.password,User.username, User.first_name, User.last_name, User.mobile, User.gender, User.joinDate).filter(User.username==username).first())

@app.route("/getUserInfo?id=<id>", methods=['GET'])
def getUserInfo(id):
    return jsonify(db.session.query(User.id, User.email, User.password,User.username, User.first_name, User.last_name, User.mobile, User.gender, User.joinDate).filter(User.id==id).first())

############
#5. userLogin
############
@app.route("/doLogin?loginType=<loginType>&account=<account>&password=<password>", methods=['GET'])
def doLogin(loginType, account, password):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    result = {'code':0, 'msg':''}
    if loginType == 1:
        if account.isnumeric() == False or len(account) != 8:
            result['code'] = 0
            result['msg'] = 'mobile phone number format is incorrect！'
            return jsonify(result)
    elif loginType == 2:
        if re.search(regex, account) == False:
            result['code'] = 0
            result['msg'] = 'Email format is incorrect！' 
            return jsonify(result)
    return jsonify(db.session.query(User.id, User.email, User.password,User.username, User.first_name, User.last_name, User.mobile, User.gender, User.joinDate).filter(User.username==account).first())

############
#6. aws send SMS
############
@app.route("/doSMSCode?loginType=<loginType>&account=<account>&code=<code>", methods=['POST'])
def doSMSCode(loginType, account, code):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    result = {'code':0, 'msg':''}
    ### SMS Type
    if loginType == 1:
        if account.isnumeric() == False or len(account) != 8:
            result['code'] = 0
            result['msg'] = 'mobile phone number format is incorrect！'
            return jsonify(result)
        result['msg'] = aws.sendSMSCode(account,code)
    ### Email Type
    elif loginType == 2:
        if re.search(regex, account) == False:
            result['code'] = 0
            result['msg'] = 'Email format is incorrect！' 
            return jsonify(result)
        result['msg'] = aws.sendEmailCode(account,code,"Hong Kong")
    result['code'] = 1
    return jsonify(result)

#data.fill_gender()
#data.fill_data()
    
db.create_all()