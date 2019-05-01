import uuid

from app.api import api
from app import db
from app.models import (
    Cart
)
from flask import (
    g,
    jsonify,
    session
)


@api.before_app_request
def before_request():
    if 'cart_id' in session:
        g.cart_id = session['cart_id']
    else:
        g.cart_id = str(uuid.uuid4())
        session['cart_id'] = g.cart_id
    g.cart = Cart.query.filter_by(id=g.cart_id).first()
    if g.cart is None:
        g.cart = Cart(id=g.cart_id)
        db.session.add(g.cart)


@api.route('/api/cartcomponent/')
def get_cart_quantity():
    cart_items = g.cart.cart_items
    cart_quantity = sum([item.amount for item in cart_items])
    return jsonify({'quantity': cart_quantity})