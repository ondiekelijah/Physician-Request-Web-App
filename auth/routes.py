from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from .forms import *
from . import *
from wtforms import ValidationError, validators
from main_app import db, bcrypt, login_manager
from flask import current_app
from flask_login import (
    UserMixin,
    login_required,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
    send_from_directory,
)
from werkzeug.routing import BuildError
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from geopy.exc import GeocoderUnavailable

from utils import *
from flask_bcrypt import generate_password_hash, check_password_hash
from models import *
from geopy.geocoders import Nominatim


auth = Blueprint("auth", __name__, url_prefix="/0")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


# lOGIN route
@auth.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Username or password!", "danger")
        except:
            flash("Invalid Username or password!", "danger")

    return render_template("auth.html",
        form=form,
        legend="Login",
        title="Sound Kenya | Login",
        action="Login"
        )



# Register route
@auth.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            pwd = form.pwd.data
            email = form.email.data
            lname = form.lname.data
            fname = form.fname.data
            location= form.location.data
            sex = form.sex.data
            speciality= form.speciality.data
            
            newuser = User(
                email=email,
                lname=lname,
                fname=fname,
                location=location,
                sex=sex,
                speciality=speciality,
                pwd=bcrypt.generate_password_hash(pwd),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("auth.login"))
        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")

            
    return render_template("auth.html",
        form=form,
        legend="Create account",
        title="Sound Kenya | Register",
        action="Register account"
        )


@auth.route("/account/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def account():
    form = UpdateProfile()

    address= current_user.location
    geolocator = Nominatim(user_agent="MeDoc")
    location_coordinates = geolocator.geocode(address)
    location_coordinates = list((location_coordinates.latitude, location_coordinates.longitude))

    if form.validate_on_submit():

        try:
            if form.profileImg.data:
                picture_file = upload_img(form.profileImg.data)
                current_user.image = picture_file

        
            current_user.email = form.email.data
            current_user.fname = form.fname.data
            current_user.lname = form.lname.data
            current_user.location = form.location.data

            db.session.commit()
            flash("Your profile has been updated", "success")
            return redirect(url_for("auth.account"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
        except GeocoderUnavailable:
            db.session.rollback()
            flash(f"Network Error while fetching your location!", "danger")

    elif request.method == "GET":
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.location.data = current_user.location
        form.profileImg.data = current_user.image

    return render_template(
        "account.html",
        form=form,
        location_coordinates=location_coordinates
    )

@auth.route("/status",methods=("GET", "POST"),strict_slashes=False,)
@login_required
def toggle_status():
    user = User.query.filter_by(id=current_user.id).first()

    user.status = not user.status
    db.session.commit()
    
    return redirect(url_for('auth.account'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

