import uuid
from flask import (
    Blueprint,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
    request
)
from werkzeug.urls import url_parse
from flask_login import (
    login_user,
    logout_user,
    current_user
)
from app import db
from app.extensions import login
from app.models import Cart, Category, User
from app.accounts.forms import (
    LoginForm,
    RegistrationForm
)

account = Blueprint('account', __name__)

@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        remember_me = form.remember_me.data
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('account.login'))
        login_user(user, remember=remember_me)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.index')
        return redirect(next_page)
    categories = Category.query.order_by(Category.name.desc())
    cart_items = g.cart.cart_items
    cart_quantity = sum([item.amount for item in cart_items])

    return render_template('accounts/login.html',
                            categories=categories,
                            cart_quantity=cart_quantity,
                            title='Sign In',
                            form=form
                            )


@account.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('auth.index'))


@account.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('account.login'))
    categories = Category.query.order_by(Category.name.desc())
    cart_items = g.cart.cart_items
    cart_quantity = sum([item.amount for item in cart_items])

    return render_template('accounts/register.html',
                           categories=categories,
                           cart_quantity=cart_quantity,
                           title='Register',
                           form=form)
