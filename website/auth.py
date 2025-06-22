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
                organizationid = None

                if affiliation_type == "organization":
                    org_name = data.get("organization-name")
                    org_address = data.get("organization-address")

                    if org_name:
                        org_insert = supabase.table("organization").upsert(
                            {
                                "name": org_name,
                                "address": org_address
                            },
                            on_conflict="name",
                            returning="representation"
                        ).execute()

                        if org_insert.data and "id" in org_insert.data[0]:
                            organizationid = org_insert.data[0]["id"]
                        else:
                            raise Exception("Organization insert failed or ID missing")
                    else:
                        # fallback: don't assign organizationid if name is empty
                        organizationid = None

                if affiliation_type == "school":
                    schoolid = int(data.get("school-name"))  # Direct ID from dropdown

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

            # ✅ Auto-create Membership Registration Record
            supabase.table("membershipregistration").insert({
                "memberid": memberid,
                "typeid": 1,
                # HARDCODE
                "status": "Pending",
                "startdate": None,
                "enddate": None
            }).execute()

        except Exception as nested_error:
            supabase.table("member").delete().eq("memberid", memberid).execute()
            raise nested_error

        # After all registration logic and inserts succeed:
        session['user_type'] = 'member'
        session['member_id'] = memberid

        if role == 'individual' and affiliation_type == 'not_applicable':
            return jsonify({'redirect': '/billing'})
        elif role == 'individual' or role == 'institution':
            return jsonify({'redirect': '/auth/login'})
        else:
            return jsonify({'error': 'Unknown registration result'}), 400


    except Exception as e:
        print("Registration error:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# -- AUTH LOGOUT --
@auth.route('auth/logout', methods=['POST'])
def logout():
    session.clear()  # Clears all session keys
    return redirect('/')

# @auth.route('/auth/login', methods=['POST'])
# def login():
#     data = request.json or {}
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({'error': 'Email and password are required'}), 400

#     # 1. Try to log in as MEMBER
#     member_response = supabase.table('member').select('*').eq('email', email).execute()
#     if member_response.data:
#         member = member_response.data[0]

#         if not check_password_hash(member['password'], password):
#             return jsonify({'error': 'Invalid credentials'}), 401

#         memberid = member['memberid']
#         role = member['role']
#         status = member['status']

#         # Check if member is active
#         if status != 'active':
#             return jsonify({'error': 'Your account is not active.'}), 403

#         if role == 'institution':
#             session['user_type'] = 'institution'
#             session['member_id'] = memberid
#             return jsonify({
#                 'message': 'Login successful',
#                 'user': {
#                     'memberid': memberid,
#                     'email': email,
#                     'user_type': 'institution'
#                 }
#             }), 200

#         elif role == 'individual':
#             # Get individual's data
#             individual_resp = supabase.table('individual').select('*').eq('memberid', memberid).execute()
#             if not individual_resp.data:
#                 return jsonify({'error': 'Individual profile not found'}), 404

#             individual = individual_resp.data[0]
#             affiliation = individual['affiliationtype']

#             # Check membershipregistration status (must be 'Active', not 'Pending')
#             registration_resp = supabase.table("membershipregistration")\
#                 .select("status")\
#                 .eq("memberid", memberid)\
#                 .order("membershipregistrationid", desc=True)\
#                 .limit(1)\
#                 .execute()

#             if not registration_resp.data or registration_resp.data[0]['status'] != 'Active':
#                 return jsonify({'error': 'Your registration is still pending approval.'}), 403

#             # If affiliated (organization or school)
#             if affiliation in ['organization', 'school']:
#                 institution_id = individual['organizationid'] if affiliation == 'organization' else individual['schoolid']

#                 # Get institution's memberid
#                 institution_resp = supabase.table("institutional").select("memberid").eq(
#                     'organizationid' if affiliation == 'organization' else 'schoolid',
#                     institution_id
#                 ).execute()

#                 if not institution_resp.data:
#                     return jsonify({'error': 'Your institution is not recognized in the system.'}), 404

#                 institution_memberid = institution_resp.data[0]['memberid']

#                 # Check if the institution has a Paid Membership bill
#                 billing_check = supabase.table("billing").select("status").eq("memberid", institution_memberid).eq("billtype", "Membership").execute().data
#                 if not any(bill['status'] == 'Paid' for bill in billing_check):
#                     return jsonify({'error': 'Your institution has not paid the membership fee yet.'}), 403

#             else:  # If not affiliated
#                 billing_check = supabase.table("billing").select("status").eq("memberid", memberid).eq("billtype", "Membership").execute().data
#                 if not any(bill['status'] == 'Paid' for bill in billing_check):
#                     return jsonify({'error': 'You have not completed your membership payment.'}), 403

#             # Passed all checks, allow login
#             session['user_type'] = 'individual'
#             session['member_id'] = memberid
#             return jsonify({
#                 'message': 'Login successful',
#                 'user': {
#                     'memberid': memberid,
#                     'email': email,
#                     'user_type': 'individual'
#                 }
#             }), 200

#     # 2. Try to log in as STAFF
#     staff_response = supabase.table("staff").select("*").eq("email", email).execute()
#     if staff_response.data:
#         staff = staff_response.data[0]

#         if not check_password_hash(staff['password'], password):
#             return jsonify({'error': 'Invalid credentials'}), 401

#         session['user_type'] = 'staff'
#         session['staff_id'] = staff['staffid']
#         return jsonify({
#             'message': 'Login successful',
#             'user': {
#                 'staffid': staff['staffid'],
#                 'email': staff['email'],
#                 'user_type': 'staff'
#             }
#         }), 200

#     return jsonify({'error': 'User not found'}), 404
