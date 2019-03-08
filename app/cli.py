'''
import os
import click

from glob import glob
from subprocess import call
from app import db
from app.models import (
    CatalogItem,
    Category,
    Permission,
    Role,
    User
)
import config
from config import Config
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
'''