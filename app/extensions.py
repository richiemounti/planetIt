import os

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from sqlalchemy_searchable import SearchQueryMixin
from flask_mail import Mail
from flask_session import Session


db = SQLAlchemy()
bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login = LoginManager()
login.login_view = 'account.login'
login.login_message = ('Please log in to access this page.')
mail = Mail()