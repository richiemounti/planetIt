from app.api import api
from app import db
from app.decorators import demo_admin_required, admin_required
from app.models import CatalogItem
from flask import (
    jsonify,
    request,
)
from flask_login import login_required
from sqlalchemy import func


@api.route('/catalogitems', defaults={'query': None})
@login_required
@demo_admin_required
def get_catalog_items(query):
    query = request.args.get('query')
    catalog_item_query = CatalogItem.query

    if query:
        catalog_item_query = \
            catalog_item_query.filter(func.lower(CatalogItem.first_name).contains(func.lower(query)) |
                                      func.lower(CatalogItem.last_name).contains(func.lower(query)))

    catalog_items = catalog_item_query.all()
    response = jsonify([catalog_item.to_dict() for catalog_item in
                        catalog_items])
    return response


@api.route('/catalogitems/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_catalog_item(id):
    CatalogItem.query.filter_by(id=id).delete()
    db.session.commit()

    response = jsonify({'data': 'success'})
    return response, 204