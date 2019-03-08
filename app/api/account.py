from app.api import api
from app.models import User
from flask import jsonify, request
from flask_login import login_user


@api.route('/account', methods=['POST'])
def login_demo_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user.check_password(data['password']):
        login_user(user)
        return jsonify({'result': user.id})
    return jsonify({'result': 0})