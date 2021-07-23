from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    SelectField,
    StringField
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional
import email_validator
import flask_login
from flask_login import current_user
from wtforms import ValidationError
from wtforms import validators
from models import User


class login_form(FlaskForm):
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])



class register_form(FlaskForm):
    fname = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Names must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    lname = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Names must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )

    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    sex = SelectField("sex", choices=[('Male'),('Female')])
    speciality = SelectField("specialty", choices=[('Doctor'),('Nurse')])
    location = StringField(validators=[InputRequired()])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )


class UpdateProfile(FlaskForm):

    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    fname = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Names must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    lname = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Names must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    location = StringField(validators=[InputRequired()])
    profileImg = FileField(validators=[FileAllowed(["jpg", "png", "jpeg", "svg"])])


    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already in use.")