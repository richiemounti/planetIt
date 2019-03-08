import os
from flask import (
    Flask,
    current_app
)

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, Config
from app.extensions import (
    csrf_protect,
    login,
    mail,
    bcrypt
)


app = Flask(__name__)


app.secret_key = ("b'\xbc\xe1\xbe_-\xbba\x81u\xd2\x16\xf2\t\xdass'")
app.config.from_object(['DevelopmentConfig'])
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:mulama@localhost:5432/carthagedb"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt.init_app(app)
login.init_app(app)
csrf_protect.init_app(app)
mail.init_app(app)

from app.views.auth import bp
from app.accounts.account import account
from app.admin.admin import admin
from app.cart.cart import cart
from app.catalog.catalog import catalog
from app.order.order import order
from app.api import api

app.register_blueprint(bp)
app.register_blueprint(account)
app.register_blueprint(admin)
app.register_blueprint(cart)
app.register_blueprint(catalog)
app.register_blueprint(order)
app.register_blueprint(api)