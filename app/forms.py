# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age')
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    submit = SubmitField('Register')