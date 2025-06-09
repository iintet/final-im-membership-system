from flask import Blueprint, jsonify, render_template
from . import models
from flask import current_app
from .supabase_client import supabase

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("front_page.html")

@views.route('/members', methods=['GET'])
def members_list():
    member, error = models.get_all_members(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(member), 200