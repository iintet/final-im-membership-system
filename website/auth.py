from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .supabase_client import supabase

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    try:
        response = supabase.auth.sign_in({
            'email': email,
            'password': password
        })
        if response.get('error'):
            return jsonify({"error": response['error']['message']}), 401
        
        return jsonify({
            "message": "Login successful",
            "access_token": response['data']['access_token'],
            "user": response['data']['user']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

''' 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('emailaddress')
        password = data.get('password') #notsure
        if not email or not password:
            return jsonify({"error": "Email address and password are required"}), 400
        try:
            response = supabase.auth.sign_in_with_password({"emailaddress": email, "password": password})
            if response.user:
                return redirect(url_for('views.home'))
            else:
                 return jsonify({"error": "Invalid credentials"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 400  
    else:
        return render_template('login.html')
'''

@auth.route('/logout', methods=['POST'])
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        email = data.get('emailaddress')
        password = data.get('password')
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        try:
            response = supabase.auth.sign_up({"emailaddress": email, "password": password})
            if response.user:
                return redirect(url_for('auth.login'))
            else:
                return jsonify({"error": "Signup failed"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return render_template('register.html')
