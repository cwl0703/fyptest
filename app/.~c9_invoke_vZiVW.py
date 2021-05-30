import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from flask_appbuilder import Model

class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

class Country(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name
        
    
class Department(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Function(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Benefit(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

assoc_benefits_employee = Table('benefits_employee', Model.metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('benefit_id', Integer, ForeignKey('benefit.id')),
                                  Column('employee_id', Integer, ForeignKey('employee.id'))
)


def today():
    return datetime.datetime.today().strftime('%Y-%m-%d')


class EmployeeHistory(Model):
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship("Employee")
    begin_date = Column(Date, default=today)
    end_date = Column(Date)


class Employee(Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    address = Column(Text(250), nullable=False)
    fiscal_number = Column(Integer, nullable=False)
    employee_number = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    function_id = Column(Integer, ForeignKey('function.id'), nullable=False)
    function = relationship("Function")
    benefits = relationship('Benefit', secondary=assoc_benefits_employee, backref='employee')

    begin_date = Column(Date, default=datetime.date.today(), nullable=True)
    end_date = Column(Date, default=datetime.date.today(), nullable=True)

    def __repr__(self):
        return self.full_name

class MenuItem(Model):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    link = Column(String(150), nullable=False)
    menu_category_id = Column(Integer, ForeignKey('menu_category.id'), nullable=False)
    menu_category = relationship("MenuCategory")

class MenuCategory(Model):
    __tablename__ = 'menu_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class News(Model):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    date = Column(Date, default=datetime.date.today(), nullable=True)
    newsCat_id = Column(Integer, ForeignKey('news_category.id'), nullable=False)
    newsCat = relationship("NewsCategory")

class NewsCategory(Model):
    __tablename__ = 'news_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    
class Item_category(Model):
    __tablename__ = 'item_catagory'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String(150), nullable=False)
    
    def __repr__(self):
        return (self.id,self.name,self.url)
    
class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address =  Column(String(564), default='Street ')
    birthday = Column(Date)
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'))
    contact_group = relationship("ContactGroup")

    def __repr__(self):
        return self.name


# our models
class CUser(Model):
    __tablename__ = 'cuser'
    id = Column(Integer, primary_key=True)
    password = Column(String(20), nullable=False)
    cuserTypeID = Column(Integer, ForeignKey('cusertype.id'), nullable=True)
    cusertype = relationship("CUserType")
    cuserName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(20), nullable=False)
    bio = Column(Text, nullable=True)
    mobile = Column(Integer, nullable=True)
    gender = Column(String(1), nullable=False)
    joinDate = Column(Date, default=datetime.date.today(), nullable=True)

    def __repr__(self):
        return self.full_name

# def add_column(engine, table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(engine.dialect)
#     engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

# column = Column('new_column_name', String(100), primary_key=True)
# add_column(engine, table_name, column)


class CUserType(Model):
    __tablename__ = 'cusertype'
    id = Column(Integer, primary_key=True)
    userType = Column(String(20), nullable=False)

    def __repr__(self):
        return self.name


class CRole(Model):
	__tablename__ = 'crole'
	id = Column(Integer, primary_key=True)
	userType = Column(String(6), nullable=False)
	def __repr__(self):
	    return self.name
	    


class Review(Model):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('cuser.id'), nullable=True)
    user = relationship("CUser")
    roleID = Column(Integer, ForeignKey('crole.id'), nullable=True)
    role = relationship("CRole")   
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    createdDate = Column(Date, default=datetime.date.today(), nullable=True)
    
    def __repr__(self):
        return self.name


class Region(Model):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    regionName = Column(String(50), unique = True, nullable=False)
    countryID = Column(Integer, ForeignKey('country.id'), nullable=True)
    country = relationship("Country") 

    def __repr__(self):
        return self.name


class Address(Model):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    addressLine1 = Column(Text, nullable=True)
    addressLine2 = Column(Text, nullable=True)
    regionID = Column(Integer, ForeignKey('region.id'), nullable=True)
    region = relationship("Region", backref="address")      

    def __repr__(self):
        return self.name


class AddressBook(Model):     #composite primary and foreign keys 
    __tablename__ = 'addressbook'
    userID = Column(Integer, ForeignKey('cuser.id'), primary_key=True)
    user = relationship("CUser", backref="addressbook")      
    addressID = Column(Integer, ForeignKey('address.id'), primary_key=True)
    address = relationship("Address", backref="addressbook") 

    def __repr__(self):
        return self.name


class Category(Model):     #not sure 
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    parentCategoryID = Column(Integer, ForeignKey('category.id'), nullable=True)
    category = relationship("Category")      
    name = Column(String(50), nullable=False)
    url = Column(String(150), nullable=False)
    
    def __repr__(self):
        return (self.id,self.name,self.url)


class Brand(Model):   
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    brandName = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name

class ItemStatus(Model):   
    __tablename__ = 'itemstatus'
    id = Column(Integer, primary_key=True)
    brandName = Column(String(8), nullable=False)

    def __repr__(self):
        return self.name


class Condition(Model):   
    __tablename__ = 'condition'
    id = Column(Integer, primary_key=True)
    brandName = Column(String(4), nullable=False)

    def __repr__(self):
        return self.name


class Item (Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('cuser.id'), nullable=True, primary_key=True)
    user = relationship("CUser", backref="item")
    categoryID = Column(Integer, ForeignKey('category.id'), nullable=True)
    category = relationship("Category")
    itemName = Column(String(50), nullable=False)
    brandID = Column(Integer, ForeignKey('brand.id'), nullable=True)
    brand = relationship("Brand", backref="item")
    price = Column(Integer, nullable=False)
    itemDescription = Column(Text, nullable=True)
    photoURL = Column(String, nullable=True) 
    itemStatusID = Column(Integer, ForeignKey('itemstatus.id'), nullable=True)
    itemstatus = relationship("ItemStatus")
    conditionID = Column(Integer, ForeignKey('condition.id'), nullable=True)
    condition = relationship("Condition")   
    createDate = Column(Date, default=datetime.date.today(), nullable=True)
    viewCounter = Column(Integer, nullable=False)

    def __repr__(self):
        return self.name


class Message(Model):  
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('cuser.id'), nullable=True)
    user = relationship("CUser", backref="Message")
    itemID = Column(Integer, ForeignKey('item.id'), nullable=True)
    item = relationship("Item", backref="Message")
    brandName = Column(String(8), nullable=False)
    createDate = Column(Date, default=datetime.date.today(), nullable=True)
    message = Column(Text, nullable=True)

    def __repr__(self):
        return self.name


class Like(Model):     #composite primary and foreign keys    
    __tablename__ = 'like'
    userID = Column(Integer, ForeignKey('cuser.id'), primary_key=True)
    user = relationship("CUser", backref="Like")
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="Like")

    def __repr__(self):
        return self.name


class OfferStatus(Model): 
    __tablename__ = 'offerstatus'
    id = Column(Integer, primary_key=True)
    offerStatus = Column(String(8), nullable=False)

    def __repr__(self):
        return self.name


class Offer(Model):     #composite primary and foreign keys     
    __tablename__ = 'offer'
    buyerID = Column(Integer, ForeignKey('cuser.id'), primary_key=True)
    user = relationship("CUser", backref="Offer")
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="Offer")
    offerDate = Column(Date, default=datetime.date.today(), primary_key=True)
    offer = Column(Integer, nullable=False) 
    offerStatusID = Column(Integer, ForeignKey('offerstatus.id'), nullable=True)
    offerstatus = relationship("OfferStatus", backref="Offer")

    def __repr__(self):
        return self.name


class PaymentMethod(Model): 
    __tablename__ = 'paymentmethod'
    id = Column(Integer, primary_key=True)
    paymentMethod= Column(String(16), nullable=False)

    def __repr__(self):
        return self.name


class AvailablePaymentMethod(Model): 
    __tablename__ = 'availablepaymentmethod'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    paymentMethodID = Column(Integer, ForeignKey('paymentmethod.id'), primary_key=True)
    paymentmethod = relationship("PaymentMethod")
    remarks = Column(Text, nullable="True")

    def __repr__(self):
        return self.name


class DeliveryMethod(Model): 
    __tablename__ = 'deliverymethod'
    id = Column(Integer, primary_key=True)
    deliveryMethod= Column(String(9), nullable=False)

    def __repr__(self):
        return self.name


class AvailableDeliveryMethod(Model): 
    __tablename__ = 'availabledeliverymethod'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    deliveryMethodID = Column(Integer, ForeignKey('deliverymethod.id'), primary_key=True)
    deliverymethod = relationship("DeliveryMethod")
    remarks = Column(Text, nullable="True")

    def __repr__(self):
        return self.name


class CarBody(Model): 
    __tablename__ = 'carbody'
    id = Column(Integer, primary_key=True)
    carbody= Column(String(13), nullable=False)

    def __repr__(self):
        return self.name


class CarTransmission(Model): 
    __tablename__ = 'cartransmission'
    id = Column(Integer, primary_key=True)
    carTransmission = Column(String(6), nullable=False)

    def __repr__(self):
        return self.name


class CarInfo(Model): 
    __tablename__ = 'carinfo'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="CarInfo")
    carBodyID = Column(Integer, ForeignKey('carbody.id'))
    carbody = relationship("CarBody", backref="CarInfo")
    carTransmissionID = Column(Integer, ForeignKey('cartransmission.id'))
    cartransmission = relationship("CarTransmission", backref="CarInfo")
    ownerCount = Column(Integer, nullable=False)
    seats = Column(Integer, nullable=False)

    def __repr__(self):
        return self.name


class PropertyType(Model): 
    __tablename__ = 'propertytype'
    id = Column(Integer, primary_key=True)
    propertyType = Column(String(20), nullable=False)

    def __repr__(self):
        return self.name


class PropertyLevel(Model): 
    __tablename__ = 'propertylevel'
    id = Column(Integer, primary_key=True)
    propertyLevel = Column(String(9), nullable=False)

    def __repr__(self):
        return self.name


class Furnishing(Model): 
    __tablename__ = 'furnishing'
    id = Column(Integer, primary_key=True)
    furnishing = Column(String(7), nullable=False)

    def __repr__(self):
        return self.name


class Facilities(Model): 
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key=True)
    facilities = Column(String(25), nullable=False)

    def __repr__(self):
        return self.name


class AvailableFacilities(Model): 
    __tablename__ = 'availablefacilities'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    facilitiesID = Column(Integer, ForeignKey('facilities.id'), primary_key=True)
    facilities = relationship("Facilities")
    remarks = Column(Text, nullable="True")

    def __repr__(self):
        return self.name


class Features(Model): 
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    features = Column(String(18), nullable=False)

    def __repr__(self):
        return self.name


class AvailableFeatures(Model): 
    __tablename__ = 'availablefeatures'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    featuresID = Column(Integer, ForeignKey('features.id'), primary_key=True)
    features = relationship("Features")
    remarks = Column(Text, nullable="True")

    def __repr__(self):
        return self.name

class PropertyInfo(Model): 
    __tablename__ = 'carinfo'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="PropertyInfo")
    
    propertyTypeID = Column(Integer, ForeignKey('propertytype.id'), primary_key=True)
    propertytype = relationship("PropertyType", backref="PropertyInfo")
    
    propertyLevelID = Column(Integer, ForeignKey('propertylevel.id'))
    propertyLevel= relationship("PropertyLevel", backref="PropertyInfo")
    
    buildingAge = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False) 
    beds = Column(Integer, nullable=False)
    baths = Column(Integer, nullable=False)
    
    furnishinghingID = Column(Integer, ForeignKey('furnishing.id'), primary_key=True)
    furnishing = relationship("Furnishing", backref="PropertyInfo")   

    def __repr__(self):
        return self.name
