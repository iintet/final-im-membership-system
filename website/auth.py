from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from .supabase_client import supabase
from werkzeug.security import generate_password_hash, check_password_hash
import re

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
    role = data.get('role')  # Get the role (individual or institution)

    try:
        # Validate and sanitize phone number
        phone_clean = clean_phone(data.get('emergencycontactnumber'))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
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
    session.clear()  # Clears all session keys
    return redirect('/')


