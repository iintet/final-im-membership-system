from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from .supabase_client import supabase
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import auth  # adjust this based on your blueprint
import logging
import traceback

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

    try:
        data = request.get_json() or {}
        print("Received registration data:", data)

        required_fields = ['email', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        email = data['email']
        password = data['password']
        role = data['role']
        affiliation_type = data.get("affiliation-type")

        # 🔍 Duplicate email check
        # 🔍 Duplicate email check with None-safe handling
        existing = supabase.table("member").select("email").eq("email", email).maybe_single().execute()

        if existing and existing.get("data"):
            return jsonify({"error": "Email already registered."}), 400


        def safe_int(val, field):
            try:
                return int(val)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid or missing value for {field}")

        # 🔧 Address handling
        if role == 'institution':
            region = safe_int(data.get("inst-region"), "region")
            province = safe_int(data.get("inst-province"), "province")
            city = safe_int(data.get("inst-city"), "city")
            barangay = safe_int(data.get("inst-barangay"), "barangay")
            street = data.get("inst-street")
            emergencycontactname = data.get('institution-emergency-contact-name')
            emergencycontactnumber = clean_phone(data.get('institution-emergencycontactnumber'))
        elif role == 'individual':
            region = safe_int(data.get("region"), "region")
            province = safe_int(data.get("province"), "province")
            city = safe_int(data.get("city"), "city")
            barangay = safe_int(data.get("barangay"), "barangay")
            street = data.get("street")
            emergencycontactname = data.get('individual-emergency-contact-name')
            emergencycontactnumber = clean_phone(data.get('individual-emergency-contact-number'))
        else:
            return jsonify({"error": "Invalid role"}), 400

        hashed_password = generate_password_hash(password)

        member_data = {
            "email": email,
            "password": hashed_password,
            "role": role,
            "status": "active",
            "region": region,
            "province": province,
            "city": city,
            "barangay": barangay,
            "streetaddress": street,
            "emergencycontactname": emergencycontactname,
            "emergencycontactnumber": emergencycontactnumber
        }

        # Optional: Handle organization
        organizationid = None
        org_name = data.get("organization-name")
        org_address = data.get("organization-address")
        if org_name:
            existing_org = supabase.table("organization").select("organizationid").eq("name", org_name).maybe_single().execute()
            if existing_org.data:
                organizationid = existing_org.data["organizationid"]
            else:
                inserted = supabase.table("organization").insert({
                    "name": org_name,
                    "address": org_address
                }).execute()
                organizationid = inserted.data[0]["organizationid"]

        # 🧩 Now we insert the member first
        member_response = supabase.table("member").insert(member_data).execute()
        if not member_response.data:
            raise Exception("Failed to insert member.")
        memberid = member_response.data[0]['memberid']

        # 🛡️ Add rollback protection
        try:
            if role == "individual":
                phone = clean_phone(data.get("phone"))
                schoolid = None

                if affiliation_type == "school":
                    school_name = data.get("school-name")
                    school_region = safe_int(data.get("school-region"), "school-region")
                    school_province = safe_int(data.get("school-province"), "school-province")
                    school_city = safe_int(data.get("school-city"), "school-city")
                    school_type = data.get("school-type")

                    school_lookup = supabase.table("school").select("schoolid") \
                        .eq("name", school_name).maybe_single().execute()
                    if school_lookup.data:
                        schoolid = school_lookup.data["schoolid"]
                    else:
                        supabase.table("school").insert({
                            "name": school_name,
                            "region": school_region,
                            "province": school_province,
                            "city": school_city,
                            "type": school_type
                        }).execute()

                        recheck = supabase.table("school").select("schoolid") \
                            .eq("name", school_name).maybe_single().execute()
                        if not recheck.data:
                            raise Exception("Failed to get school ID after insert.")
                        schoolid = recheck.data["schoolid"]

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

                supabase.table("individual").insert(individual_data).execute()

            elif role == "institution":
                inst_data = {
                    "memberid": memberid,
                    "name": data.get("institution-name"),
                    "representativelastname": data.get("rep-last-name"),
                    "representativefirstname": data.get("rep-first-name"),
                    "representativemiddlename": data.get("rep-middle-name"),
                    "representativecontactnumber": clean_phone(data.get("rep-contact")),
                    "type": data.get("institution-type")
                }

                supabase.table("institutional").insert(inst_data).execute()

        except Exception as nested_error:
            # 💣 Cleanup: rollback member if the second insert failed
            supabase.table("member").delete().eq("memberid", memberid).execute()
            raise nested_error  # re-raise to be caught by outer except

        session['user_type'] = 'member'
        session['member_id'] = memberid

        return jsonify({'message': 'Registration successful'})

    except Exception as e:
        print("Registration error:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# -- AUTH LOGOUT --
@auth.route('auth/logout', methods=['POST'])
def logout():
    session.clear()  # Clears all session keys
    return redirect('/')


