import logging, re
from flask import Flask , render_template , request, send_file,jsonify
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy.engine import Engine
from sqlalchemy import event , desc , asc
from .indexview import FABView
from .models import Item, DMUser , Category
from .aws_api import amazonApi 
import locale

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
valueList={"rr"}
app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
valueList = {"rr","bb"}
appbuilder = AppBuilder(app, db.session , base_template='mybase.html',indexview=FABView )
aws = amazonApi()

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
                itemlists2=db.session.query(Item).order_by(desc(Item.createdDate)).limit(10),
                userDetails=db.session.query(DMUser.id,DMUser.userName).all())
                         
@app.context_processor                             
def category_list():
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
    condition = item.getCondition().condition
    status = item.getStatus().itemStatus
    category = db.session.query(Category.categoryName).filter_by(id=itemId).first()
    return render_template("product/product.html",base_template='mybase.html',
                            appbuilder=appbuilder, item=item,condition=condition , 
                            status=status,category=category)
    
#Product List
#@app.route('/product_list/categoryId=<int:categoryId>', strict_slashes=False)
#@app.route('/product_list/productId=<int:productId>', strict_slashes=False)
# def getProductListByCategoryId(categoryId=None,productId=None):
#       if 
#     #database
#     #return 



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
    return jsonify(db.session.query(Item.id, Item.userID, Item.categoryID,Item.itemName, Item.price, Item.itemDescription, Item.itemStatusID, Item.viewCounter).filter(Item.id==itemId).first())
@app.route("/getProductDetail?itemName=<itemName>", methods=['GET'])
def getProductDetailByName(itemName):
    return jsonify(db.session.query(Item.id, Item.userID, Item.categoryID,Item.itemName, Item.price, Item.itemDescription, Item.itemStatusID, Item.viewCounter).filter(Item.itemName==itemName).first())
#############
#4. Profile
#############
  
@app.route("/getUser?userName=<userName>", methods=['GET'])
def getUser(userName):
    return jsonify(db.session.query(DMUser.userID, DMUser.email, DMUser.password,DMUser.userName, DMUser.firstName, DMUser.lastName, DMUser.mobile, DMUser.gender, DMUser.joinDate).filter(DMUser.userName==userName).first())

@app.route("/getUserInfo?userId=<userId>", methods=['GET'])
def getUserInfo(userId):
    return jsonify(db.session.query(DMUser.userID, DMUser.email, DMUser.password,DMUser.userName, DMUser.firstName, DMUser.lastName, DMUser.mobile, DMUser.gender, DMUser.joinDate).filter(DMUser.userID==userId).first())

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
    return jsonify(db.session.query(DMUser.userID, DMUser.email, DMUser.password,DMUser.userName, DMUser.firstName, DMUser.lastName, DMUser.mobile, DMUser.gender, DMUser.joinDate).filter(DMUser.userName==account).first())

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