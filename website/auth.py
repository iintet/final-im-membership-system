from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from .supabase_client import supabase
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import auth  # adjust this based on your blueprint
import logging

auth = Blueprint('auth', __name__)

def clean_phone(phone_str):
    # Remove spaces, dashes, and validate Philippine mobile numbers starting with 09 (11 digits)
    phone = re.sub(r'[\s\-]', '', phone_str or '')
    if not re.match(r'^09\d{9}$', phone):
        raise ValueError("Invalid phone number format. Must start with 09 and be 11 digits.")
    return phone

# -- AUTH LOGIN --
@auth.route('/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Check member table first
    member_response = supabase.table('member').select('*').eq('email', email).execute()

    if member_response.data:
        member = member_response.data[0]
        print("Logging in member:", member) 

        if check_password_hash(member['password'], password):
            session['user_type'] = 'member'
            session['member_id'] = member['memberid']

            return jsonify({
                'message': 'Login successful',
                'user': {
                    'memberid': member['memberid'],
                    'email': member['email'],
                    'role': member['role'],
                    'status': member['status'],
                    'user_type': 'member'
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    # If not a member, check staff table
    staff_response = supabase.table('staff').select('*').eq('email', email).execute()

    if staff_response.data:
        staff = staff_response.data[0]

        if check_password_hash(staff['password'], password):
            session['user_type'] = 'staff'
            session['staff_id'] = staff['staffid']

            print("Email:", email)
            print("Password:", password)
            print("Staff response:", staff_response.data)

            return jsonify({
                'message': 'Login successful',
                'user': {
                    'staffid': staff['staffid'],
                    'email': staff['email'],
                    'role': staff['role'],
                    'fullname': staff['fullname'],
                    'user_type': 'staff'
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'error': 'User not found'}), 404
    
# -- AUTH REGISTER --
@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.get_json() or {}

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        phone_clean = clean_phone(data.get('emergencycontactnumber', ''))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    user_data = {
        'email': email,
        'password': hashed_password,
        'role': role,
        'status': 'active',
        'streetaddress': data.get('streetaddress', ''),
        'emergencycontactname': data.get('emergencycontactname', ''),
        'emergencycontactnumber': phone_clean,
        'region': data.get('region'),
        'province': data.get('province'),
        'city': data.get('city'),
        'barangay': data.get('barangay')
    }

    if role == 'individual':
        user_data.update({
            'memberid': data.get('memberid'),
            'lastname': data.get('last-name'),
            'firstname': data.get('first-name'),
            'middlename': data.get('middle-name'),
            'gender': data.get('gender'),
            'dateofbirth': data.get('dob'),
            'phone': data.get('phone')
        })
    elif role == 'institution':
        user_data.update({
            'memberid': data.get('memberid'),
            'name': data.get('institution-name'),
            'representativelastname': data.get('rep-last-name'),
            'representativefirstname': data.get('rep-first-name'),
            'representativemiddlename': data.get('rep-middle-name'),
            'representativecontactnumber': data.get('rep-contact')
        })

    try:
        response = supabase.table('member').insert(user_data).execute()
        logging.info(f"Supabase insert response: {response}")

        if hasattr(response, 'error') and response.error:
            return jsonify({"error": str(response.error)}), 500

        # Optionally set session
        session['user_email'] = email

        # Redirect to dashboard
        return redirect(url_for('views.dashboard'))  # adjust 'views.dashboard' to match your route name

    except Exception as e:
        logging.error(f"Error inserting user: {e}")
        return jsonify({"error": str(e)}), 500




# -- AUTH LOGOUT --
@auth.route('auth/logout', methods=['POST'])
def logout():
    session.clear()  # Clears all session keys
    return redirect('/')


