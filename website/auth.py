from flask import Blueprint, request, jsonify
from flask_supabase import Supabase
from flask import current_app

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    return "Login"

@auth.route('/logout')
def logout():
    return "Logout"

@auth.route('/sign-up')
def signup():
    return "Sign up"
