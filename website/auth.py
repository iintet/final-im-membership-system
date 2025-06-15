from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .supabase_client import supabase
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# -- AUTH LOGIN --
@auth.route('/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    # Fetch user from the database using email
    user_response = supabase.table('member').select('*').eq('email', email).execute()
    if user_response.data:
        user = user_response.data[0]
        # Check if the provided password matches the stored hashed password
        if check_password_hash(user['password'], password):
            # Successful login
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'memberid': user['memberid'],
                    'email': user['email'],
                    'role': user['role'],
                    'status': user['status']
                }
            }), 200
        else:
            # Invalid credentials
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        # User not found
        return jsonify({'error': 'User  not found'}), 404

# -- AUTH REGISTER --
@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    data = request.get_json()
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    # Store the user in the database
    user_response = supabase.table('member').insert({
        'email': email,
        'password': hashed_password,
        'role': 'user',  # Default role
        'status': 'active',  # Default status
        'streetaddress': data.get('streetaddress', ''),
        'emergencycontactname': data.get('emergencycontactname', ''),
        'emergencycontactnumber': data.get('emergencycontactnumber', '')
    }).execute()
    if user_response.error:
        return jsonify({'error': str(user_response.error)}), 500
    return jsonify({'message': 'User registered successfully'}), 201

# -- AUTH LOGOUT --
@auth.route('auth/logout', methods=['POST'])
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


