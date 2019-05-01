import uuid
from app.extensions import csrf_protect
from app import db
from app.models import (
    Cart,
    CartItem,
    Category,
)
from flask import (
    Blueprint,
    current_app,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_login import current_user, login_required

order = Blueprint('order', __name__)

@order.before_app_request
def before_request():
    if 'cart_id' in session:
        g.cart_id = session['cart_id']
    else:
        g.cart_id = str(uuid.uuid4())
        session['cart_id'] = g.cart_id
    g.cart = Cart.query \
        .filter_by(id=g.cart_id) \
        .first()
    if g.cart is None:
        g.cart = Cart(id=g.cart_id)
        db.session.add(g.cart)


@order.route('/checkout/')
@login_required
def checkout():
    g.cart.cart_items = []
    db.session.commit()

    return redirect(url_for('order.complete'))


@order.route('/complete')
@login_required
def complete():
    categories = Category.query \
        .order_by(Category.name.desc())
    cart_items = g.cart.cart_items
    cart_quantity = sum([item.amount for item in cart_items])

    body = render_template(
        'email/order_confirmation.html', user=current_user)
    app = current_app._get_current_object()
    
    '''
    send_email(app,
               "Planet It Confirmation",
               [current_user.email],
               body)
    '''

    return render_template('order/complete.html',
                           title='Order Complete',
                           cart_quantity=cart_quantity,
                           categories=categories)


    