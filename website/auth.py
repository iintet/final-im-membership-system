from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .supabase_client import supabase

auth = Blueprint('auth', __name__)

# -- AUTH LOGIN --
@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    try:
        login_response = supabase.auth.sign_in({
            'email': email,
            'password': password
        })

        if login_response.get('error'):
            return jsonify({"error": login_response['error']['message']}), 401
        return jsonify({
            "message": "login successful",
            "access_token": login_response['data']['access_token'],
            "user": login_response['data']['user']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# -- AUTH REGISTER --
@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # 'individual' or 'institution'
    if not email or not password or not role:
        return jsonify({"error": "email, password, and role are required"}), 400
    try:
        sign_up_response = supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        if sign_up_response.get('error'):
            return jsonify({"error": sign_up_response['error']['message']}), 400
        member_data = {
            "emailaddress": email,    # match your DB column names
            "role": role,
            # include other fields from data as needed, e.g., firstname, institutionname...
        }

        insert_response = supabase.table('member').insert(member_data).execute()
        if insert_response.error:
            return jsonify({"error": insert_response.error.message}), 500
        return jsonify({"message": "registration successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -- AUTH LOGOUT --
@auth.route('auth/logout', methods=['POST'])
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


