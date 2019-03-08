from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import cart, cart_component, catalog_items, account