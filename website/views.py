from flask import Blueprint, jsonify, current_app, request, abort, render_template
from . import models
from datetime import datetime



views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("front_page.html")
