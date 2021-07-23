import secrets
import os
import bs4
import urllib, re
from PIL import Image
# from . import app
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
from flask import current_app

# image upload handler

def upload_img(doc_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(doc_img.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/img/profile_images", picture_filename
    )
    doc_img.save(picture_path)
    return picture_filename

           