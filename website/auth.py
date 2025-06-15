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
    
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # Get the role (individual or institution)
    # Common fields
    streetaddress = data.get('streetaddress', '')
    emergencycontactname = data.get('emergencycontactname', '')
    emergencycontactnumber = data.get('emergencycontactnumber', '')
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    # Prepare the user data to be inserted
    user_data = {
        'email': email,
        'password': hashed_password,
        'role': role,
        'status': 'active',  # Default status
        'streetaddress': streetaddress,
        'emergencycontactname': emergencycontactname,
        'emergencycontactnumber': emergencycontactnumber,
        'region': data.get('region'),  # Align with schema
        'province': data.get('province'),  # Align with schema
        'city': data.get('city'),  # Align with schema
        'barangay': data.get('barangay')  # Align with schema
    }
    # Handle individual fields
    if role == 'individual':
        user_data.update({
            'memberid': data.get('memberid'),  # Align with schema
            'lastname': data.get('last-name'),  # Align with schema
            'firstname': data.get('first-name'),  # Align with schema
            'middlename': data.get('middle-name'),  # Align with schema
            'gender': data.get('gender'),  # Align with schema
            'dateofbirth': data.get('dob'),  # Align with schema
            'phone': data.get('phone')  # Align with schema
        })
    # Handle institution fields
    elif role == 'institution':
        user_data.update({
            'memberid': data.get('memberid'),  # Align with schema
            'name': data.get('institution-name'),  # Align with schema
            'representativelastname': data.get('rep-last-name'),  # Align with schema
            'representativefirstname': data.get('rep-first-name'),  # Align with schema
            'representativemiddlename': data.get('rep-middle-name'),  # Align with schema
            'representativecontactnumber': data.get('rep-contact')  # Align with schema
        })
    # Store the user in the database
    user_response = supabase.table('member').insert(user_data).execute()
    if user_response.error:
        return jsonify({'error': str(user_response.error)}), 500
    return jsonify({'message': 'User  registered successfully'}), 201


# -- AUTH LOGOUT --
@auth.route('auth/logout', methods=['POST'])
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


