# Import all the required modules
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
# End of imports

# Register a blueprint for authentication 

auth = Blueprint("auth", __name__, url_prefix="/0")

# Load the user,and return the user object

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

# lOGIN route
@auth.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    # Instantiate the login_form and assign it to 
    # a variable form
    form = login_form()
    # If form is validated during submission,begin the execution
    if form.validate_on_submit():
        try:
            # get the user that exists with the submitted email
            user = User.query.filter_by(email=form.email.data).first()
            # check if the user given email matches the password
            # that is stored for that email
            if check_password_hash(user.pwd, form.pwd.data):
            #login the user
                login_user(user)
            # Redirect to the user account
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Username or password!", "danger")
        except:
            flash("Invalid Username or password!", "danger")

    return render_template("auth.html",
        form=form,
        legend="Login",
        title="MeDOC | Login",
        action="Login"
        )

# Register route
@auth.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    # Instantiate the register_form and assign it to 
    # a variable form
    form = register_form()
    # If form is validated during submission,begin the execution
    if form.validate_on_submit():
        try:
            # assign the user input values from the 
            # form variables
            pwd = form.pwd.data
            email = form.email.data
            lname = form.lname.data
            fname = form.fname.data
            location= form.location.data
            sex = form.sex.data
            speciality= form.speciality.data
            
            # create a variable to hold the user object
            newuser = User(
                email=email,
                lname=lname,
                fname=fname,
                location=location,
                sex=sex,
                speciality=speciality,
                pwd=bcrypt.generate_password_hash(pwd),
            )
            # Add user to the database
            db.session.add(newuser)
            # Save
            db.session.commit()
            # Show a success message
            flash(f"Account Succesfully created", "success")
            # Redirect to the login page
            return redirect(url_for("auth.login"))
        # Handle exceptions 
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
    # register function return statement
    return render_template("auth.html",
        form=form,
        legend="Create account",
        title="MeDOC | Register",
        action="Register account"
        )

# User account route
@auth.route("/account/", methods=("GET", "POST"), strict_slashes=False)
# Require the user to login first
@login_required
def account():
    # Instantiate the UpdateProfile and assign it to 
    # a variable form
    form = UpdateProfile()
    # assign the address as the current users location
    # location is from the location the user provided
    # address= current_user.location
    # geolocator = Nominatim(user_agent="MeDoc")
    # Geocode the address
    # location_coordinates = geolocator.geocode(address)
    # Store the longitude and latitude as a list
    # location_coordinates = list((location_coordinates.latitude, location_coordinates.longitude))

    if form.validate_on_submit():
    # If form is validated during submission,begin the execution
        try:
            # if the user has provided a profile image
            if form.profileImg.data:
                # call the image upload method and pass to it
                # the user image
                picture_file = upload_img(form.profileImg.data)
                # Update the current user image to the new image
                current_user.image = picture_file

            # Update the current user details with the new
            # data
            current_user.email = form.email.data
            current_user.fname = form.fname.data
            current_user.lname = form.lname.data
            current_user.location = form.location.data
            current_user.speciality = form.speciality.data
            # save the changes
            db.session.commit()
            # Flash a success message
            flash("Your profile has been updated", "success")
            # Redirect back
            return redirect(url_for("auth.account"))
        # Handle exeptions
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
    # Unless the request is a post request,display
    # the user details in the input fields
    elif request.method == "GET":
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.location.data = current_user.location
        form.speciality.data = current_user.speciality
        form.profileImg.data = current_user.image
    # Function return statement
    return render_template(
        "account.html",
        form=form,
        #location_coordinates=location_coordinates
    )
# Use this route to toggle the user
# online and offline status
@auth.route("/status",methods=("GET", "POST"),strict_slashes=False,)
# Require the user to login first
@login_required
def toggle_status():
    # Get the current user
    user = User.query.filter_by(id=current_user.id).first()
    # Toggle the status to the opposite of the current status
    user.status = not user.status
    # Save these changes
    db.session.commit()
    # Redirect back the user
    return redirect(url_for('auth.account'))

# Logout user route
@auth.route("/logout")
# Require the user to login first
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

