import uuid
import app
from app import db
from app.models import (
    Cart,
    Category,
)

from flask import (
    Blueprint, request,  render_template, make_response, abort, g, session
)

bp = Blueprint('auth', __name__)

from app.views import Views



@bp.before_app_request
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

@bp.route('/')
@bp.route('/index')
def index():
    categories = Category.query.order_by(Category.name.desc())
    cart_items = g.cart.cart_items
    cart_quantity = sum([item.amount for item in cart_items])

    return render_template('auth/index.html',
                            title='Main',
                            categories=categories,
                            cart_quantity=cart_quantity
                            )