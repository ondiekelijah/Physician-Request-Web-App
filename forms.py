from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    SelectField
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
import email_validator
import flask_login
from flask_login import current_user
from wtforms import ValidationError
from wtforms import validators


class AddSpare(FlaskForm):
    spare_img = FileField(validators=[FileAllowed(["jpg", "png", "jpeg", "svg","webp"])])
    name = StringField(validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField(validators=[InputRequired()])



class GetQuote(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(1, 64)])
    email = StringField(validators=[InputRequired(),Email(), Length(1, 64)])
    phone_number = StringField(validators=[InputRequired(),Length(1, 64)])
    branch = SelectField(choices=[('Naivasha'),('Gilgil'),('Industrial area')])
    model = SelectField(choices=[('Toyota'),('Nissan'),('Mazda'),('BMW'),('Peugot'),('Honda')])

