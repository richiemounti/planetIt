from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DecimalField,
    SubmitField,
    SelectField
)
from wtforms.validators import DataRequired

class CatalogItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image_url = StringField('Image Upload', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Save')