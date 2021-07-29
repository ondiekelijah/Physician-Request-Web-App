# Import all the required modules
from flask import Blueprint
from flask import current_app
from main_app import create_app
from main_app import login_manager
from models import *
from forms import *
from utils import *

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
)
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from werkzeug.routing import BuildError
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from geopy.geocoders import Nominatim
from geopy import distance

import gi
gi.require_version('Geoclue', '2.0')
from gi.repository import Geoclue
from PIL import Image
# End imports

# Assign app to be equal to flask create_app method
app = create_app()

# Load the user,and return the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------------- MAIN APP ROUTES -----------------------------

# Home route
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    # Fetch all users
    users = User.query.order_by(User.id.desc()).all()

    # Begin estimation of the difference between the
    # patient and the physician

    clue = Geoclue.Simple.new_sync('something',Geoclue.AccuracyLevel.EXACT,None)
    patient_location = clue.get_location()

    patient_lat = patient_location.get_property('latitude')
    patient_long = patient_location.get_property('longitude')

    dist_margin= []

    # I commented this part since it never gave the expected results

    # for user in users:
    #     address= user.location
    #     geolocator = Nominatim(user_agent="MeDoc")
    #     location_coordinates = geolocator.geocode(address)

    #     physician_lat = location_coordinates.latitude
    #     physician_long = location_coordinates.longitude


    #     patient = (patient_lat, patient_long)
    #     physician = (physician_long, physician_long)


    #     dist_diff = distance.distance(patient, physician).km

    #     dist_margin.append(dist_diff)

    
    return render_template("index.html",title="MeDOC | Home",users=users,dist_margin=dist_margin)

# Logged in user dashboard route
@app.route("/dashboard", methods=("GET", "POST"), strict_slashes=False)
@login_required
def dashboard():
    return render_template("dashboard.html",title="MeDOC | Dashboard")

if __name__ == "__main__":
    app.run(debug=True)
