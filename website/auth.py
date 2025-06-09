from flask import Blueprint, request, jsonify, render_template
from .supabase_client import supabase

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form  # or request.get_json() for JSON body
        print(data)

        # Example: Authenticate with Supabase (optional logic)
        # email = data.get('email')
        # password = data.get('password')
        # response = supabase.auth.sign_in_with_password({ "email": email, "password": password })
        # return jsonify(response), 200

    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    # You can optionally call supabase.auth.sign_out() here
    return "Logout"

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        # Handle user registration logic
    return "Sign up"