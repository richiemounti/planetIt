from datetime import datetime
from app.extensions import login, bcrypt
from flask_login import AnonymousUserMixin, UserMixin
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Sequence
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils import TSVectorType
from app import db


db.configure_mappers()
make_searchable(db.metadata)



class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.String, primary_key=True)

    cart_items = db.relationship(
        'CartItem'
    )
    

class Permission:
    GENERAL = 0
    DEMO_ADMINISTER = 1
    ADMINISTER = 2

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles ={
            'User': (Permission.GENERAL, 'main', True),
            'DemoAdministrator': (Permission.DEMO_ADMINISTER, 'demo_admin', False),
            'Administrator': (Permission.ADMINISTER, 'admin', False)
        }
        for x in roles:
            role = Role.query.filter_by(name=x).first()
            if role is None:
                role = Role(name=x)
            role.permissions = roles[x][0]
            role.index = roles[x][1]
            role.default = roles[x][2]
            db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, email, role=None, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        if role:
            self.role = role
        
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None 

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.generate_password_hash(self.password, len(value))

    def can(self, permisions):
        return self.role.permissions >= permisions

    def is_demo_admin(self):
        return self.can(Permission.DEMO_ADMINISTER)

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False
    
    def is_demo_admin(self):
        return False

class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    price = db.Column(db.Numeric)

    catalog_item = db.relationship(
        'CatalogItem',
    )

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_total = db.Column(db.Numeric)
    order_placed = db.Column(db.DateTime, default=datetime.utcnow)
    order_detail_id = db.Column(db.Integer, db.ForeignKey('order_details.id'))

    order_lines = db.relationship(
        'OrderDetail',
    )

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    catalog_items = db.relationship(
        'CatalogItem',
        backref='category'
    )

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    cart_id = db.Column(db.String, db.ForeignKey('carts.id'))
    catalog_item_id = db.Column(db.Integer, db.ForeignKey('catalog_items.id', ondelete='CASCADE'))
    
    catalog_item = db.relationship(
        'CatalogItem'
    )

class CatalogItemQuery(BaseQuery, SearchQueryMixin):
    pass

class CatalogItem(db.Model):
    query_class = CatalogItemQuery
    __tablename__ = 'catalog_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    description = db.Column(db.String(140))
    image_url = db.Column(db.String(140))
    price = db.Column(db.Numeric)
    order_detail_id = db.Column(db.Integer, db.ForeignKey('order_details.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    search_vector = db.Column(TSVectorType('name'))

    def from_dict(self, data):
        for field in ['name', 'description', 'image_url',
                      'category_id', 'price']:
            if field in data:
                setattr(self, field, data[field])


    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'category_id': self.category_id,
            'price': str(self.price),
        }
        return data


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


