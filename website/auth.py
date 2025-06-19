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

    # Validation
    if not email or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Clean emergency contact
        if role == 'individual':
            emergencycontactname = data.get('individual-emergency-contact-name')
            emergencycontactnumber = clean_phone(data.get('individual-emergency-contact-number'))
        elif role == 'institution':
            emergencycontactname = data.get('institution-emergency-contact-name')
            emergencycontactnumber = clean_phone(data.get('institution-emergencycontactnumber'))
        else:
            return jsonify({"error": "Invalid role"}), 400

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert into member
        member_data = {
            "email": email,
            "password": hashed_password,
            "role": role,
            "status": "active",
            "region": int(data.get("region")),
            "province": int(data.get("province")),
            "city": int(data.get("city")),
            "barangay": int(data.get("barangay")),
            "streetaddress": data.get("street"),
            "emergencycontactname": emergencycontactname,
            "emergencycontactnumber": emergencycontactnumber
        }
        organization_name = data.get('organization-name')
        organization_address = data.get('organization-address')

        existing_org = supabase.table("organization") \
            .select("organizationid") \
            .eq("name", organization_name) \
            .maybe_single() \
            .execute()

        if existing_org.data:
            organizationid = existing_org.data['organizationid']
        else:
            # Insert and get the new ID
            org_insert = supabase.table("organization").insert({
                "name": organization_name,
                "address": organization_address
            }).execute()
            organizationid = org_insert.data[0]['organizationid']
        existing_org = supabase.table("organization") \
            .select("organizationid") \
            .eq("name", organization_name) \
            .maybe_single() \
            .execute()

        if existing_org.data:
            organizationid = existing_org.data['organizationid']
        else:
            # Insert and get the new ID
            org_insert = supabase.table("organization").insert({
                "name": organization_name,
                "address": organization_address
            }).execute()
            organizationid = org_insert.data[0]['organizationid']
        member_response = supabase.table("member").insert(member_data).execute()
        if not member_response.data:
            raise Exception("Failed to insert member. No data returned from Supabase.")

        schoolid = None
        schoolid = None
        
        
        # ✅ Get the generated memberid
        memberid = member_response.data[0]['memberid']

        # Insert into role-specific table
        if role == 'individual':
            phone = clean_phone(data.get('phone'))
            affiliation_type = data.get('affiliation-type')
            schoolid = data.get('school-name') if affiliation_type == 'school' else None
            
            schoolid = None
        if affiliation_type == 'school':
            school_name = data.get('school-name')
            school_region = int(data.get('school-region'))
            school_province = int(data.get('school-province'))
            school_city = int(data.get('school-city'))
            school_type = data.get('school-type')

            # Check if the school already exists
            existing_school = supabase.table("school") \
                .select("schoolid") \
                .eq("name", school_name) \
                .maybe_single() \
                .execute()

            if existing_school.data:
                schoolid = existing_school.data['schoolid']
            else:
                # Insert school and fetch the generated ID again
                supabase.table("school").insert({
                    "name": school_name,
                    "region": school_region,
                    "province": school_province,
                    "city": school_city,
                    "type": school_type
                }).execute()

                # Now re-fetch the schoolid
                schoolid_lookup = supabase.table("school") \
                    .select("schoolid") \
                    .eq("name", school_name) \
                    .maybe_single() \
                    .execute()
        
        if schoolid_lookup.data:
            schoolid = schoolid_lookup.data['schoolid']
        else:
            raise Exception("Failed to retrieve schoolid after insertion.")
        
        individual_data = {
            "memberid": memberid,
            "lastname": data.get("last-name"),
            "firstname": data.get("first-name"),
            "middlename": data.get("middle-name"),
            "gender": data.get("gender"),
            "dateofbirth": data.get("dob"),
            "phone": phone,
            "affiliationtype": affiliation_type,
            "schoolid": schoolid,
            "organizationid": organizationid
        }

        individual_response = supabase.table("individual").insert(individual_data).execute()
        if not individual_response.data:
            raise Exception(individual_response.error)

        elif role == 'institution':
            inst_data = {
                "memberid": memberid,
                "name": data.get("institution-name"),
                "representativelastname": data.get("rep-last-name"),
                "representativefirstname": data.get("rep-first-name"),
                "representativemiddlename": data.get("rep-middle-name"),
                "representativecontactnumber": clean_phone(data.get("rep-contact")),
                "type": data.get("institution-type")
            }

            inst_response = supabase.table("institutional").insert(inst_data).execute()
            if not inst_response.data:
                raise Exception(inst_response.error)

        # Optional: Set session
        session['user_type'] = 'member'
        session['member_id'] = memberid

        return jsonify({"message": "Registration successful", "memberid": memberid}), 200

    except Exception as e:
        print("❌ Registration failed:", e)
        return jsonify({"error": "Failed to register user"}), 500


# -- AUTH LOGOUT --
@auth.route('auth/logout', methods=['POST'])
def logout():
    session.clear()  # Clears all session keys
    return redirect('/')


