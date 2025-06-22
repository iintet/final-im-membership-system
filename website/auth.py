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

def safe_int(val, field):
    try:
        return int(val) if val not in (None, '', 'None') else None
    except (ValueError, TypeError):
        raise ValueError(f"Invalid or missing value for {field}")

# -- AUTH LOGIN --
@auth.route('/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # --- Check if INDIVIDUAL ---
    individual_response = supabase.table('member').select('*').eq('email', email).eq('role', 'individual').execute()

    if individual_response.data:
        individual = individual_response.data[0]
        if check_password_hash(individual['password'], password):
            session.clear()
            session['user_type'] = 'individual'
            session['member_id'] = individual['memberid']

            return jsonify({
                'message': 'Login successful',
                'user': {
                    'memberid': individual['memberid'],
                    'email': individual['email'],
                    'role': individual['role'],
                    'user_type': 'individual'
                },
                'redirect_to': '/user/dashboard'
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    # --- Check if INSTITUTION ---
    institution_response = supabase.table('member').select('*').eq('email', email).eq('role', 'institution').execute()

    if institution_response.data:
        institution = institution_response.data[0]
        if check_password_hash(institution['password'], password):
            session.clear()
            session['user_type'] = 'institution'
            session['member_id'] = institution['memberid']

            return jsonify({
                'message': 'Login successful',
                'user': {
                    'memberid': institution['memberid'],
                    'email': institution['email'],
                    'role': institution['role'],
                    'user_type': 'institution'
                },
                'redirect_to': '/institutional/dashboard'
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    # --- Check if STAFF ---
    staff_response = supabase.table('staff').select('*').eq('email', email).execute()

    if staff_response.data:
        staff = staff_response.data[0]
        if check_password_hash(staff['password'], password):
            session['user_type'] = 'staff'
            session['staff_id'] = staff['staffid']

            return jsonify({
                'message': 'Login successful',
                'user': {
                    'staffid': staff['staffid'],
                    'email': staff['email'],
                    'role': staff['role'],
                    'fullname': staff['fullname'],
                    'user_type': 'staff'
                },
                'redirect_to': '/staff/dashboard'
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
        affiliation_type = data.get("individual-affiliation-type")

        hashed_password = generate_password_hash(password)  # <-- Move this up here

        # 🔍 Duplicate email check
        existing = supabase.table("member").select("email").eq("email", email).maybe_single().execute()
        if existing and existing.get("data"):
            return jsonify({"error": "Email already registered."}), 400

        # 🔧 Address handling
        if role == 'institution':
            region = safe_int(data.get("inst-region"), "region")
            province = safe_int(data.get("inst-province"), "province")
            city = safe_int(data.get("inst-city"), "city")
            barangay = safe_int(data.get("inst-barangay"), "barangay")
            street = data.get("inst-street")
            emergencycontactname = data.get('emergency-contact-name-inst')
            emergencycontactnumber = clean_phone(data.get('emergency-contact-number-inst'))

            # After assigning region, province, city, barangay
            required_int_fields = {
                "region": region,
                "province": province,
                "city": city,
                "barangay": barangay
            }
            for field, value in required_int_fields.items():
                if value is None:
                    return jsonify({"error": f"{field} is required and must be selected."}), 400

            member_data = {
                "email": email,
                "password": hashed_password,
                "role": role,
                "region": region,
                "province": province,
                "city": city,
                "barangay": barangay,
                "streetaddress": street,
                "emergencycontactname": emergencycontactname,
                "emergencycontactnumber": emergencycontactnumber
            }

        elif role == 'individual':
            region = safe_int(data.get("region"), "region")
            province = safe_int(data.get("province"), "province")
            city = safe_int(data.get("city"), "city")
            barangay = safe_int(data.get("barangay"), "barangay")
            street = data.get("street")
            emergencycontactname = data.get("individual-emergency-contact-name")
            emergencycontactnumber = data.get("individual-emergency-contact-number")

            required_inst_fields = {
                "region": region,
                "province": province,
                "city": city,
                "barangay": barangay
            }
            for field, value in required_inst_fields.items():
                if value is None:
                    return jsonify({"error": f"{field} is required and must be selected."}), 400

            print("region:", region, type(region))
            print("province:", province, type(province))
            print("city:", city, type(city))
            print("barangay:", barangay, type(barangay))

            member_data = {
                "email": email,
                "password": hashed_password,
                "role": role,
                "region": region,
                "province": province,
                "city": city,
                "barangay": barangay,
                "streetaddress": street,
                "emergencycontactname": emergencycontactname,
                "emergencycontactnumber": emergencycontactnumber
            }
    
        else:
            return jsonify({"error": "Invalid role"}), 400

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
                        organizationid = None

                if affiliation_type == "school" and not data.get("school-name"):
                    school_insert = supabase.table("schname").insert({
                        "name": data.get("ind-school-name"),
                        "cityid": int(data.get("ind-school-city")),
                        "typeid": schooltype
                    }).execute()
                    schoolid = school_insert.data[0]["id"]


                # --- FIX: Always run safe_int here, after all assignments ---
                schoolid = safe_int(schoolid, "schoolid")
                organizationid = safe_int(organizationid, "organizationid")

                if affiliation_type in ("organization", "school", "none", "not_applicable"):
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
                    print("individual_data:", individual_data)
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
                
                print("region:", region, type(region))
                print("province:", province, type(province))
                print("city:", city, type(city))
                print("barangay:", barangay, type(barangay))
                print("member_data:", member_data)
                # For individual:
                print("individual_data:", individual_data)
                # For institution:
                print("inst_data:", inst_data)

                
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
#             registration_resp = supabase.table "membershipregistration")\
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
#                 institution_resp = supabase.table "institutional").select("memberid").eq(
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
