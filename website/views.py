from flask import Blueprint, jsonify, render_template, abort, request, session, redirect
from . import models
from .supabase_client import supabase
from datetime import datetime
import logging
from werkzeug.security import check_password_hash, generate_password_hash

views = Blueprint('views', __name__)

def iso_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except:
        return None
    
def validate_required_fields(data, fields):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        abort(jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400)

@views.route('/')
def home():
    return render_template("front_page.html")

@views.route('/register')
def register():
    return render_template('register.html')

@views.route('auth/login', methods=['GET'])
def login():
    return render_template('login.html')

@views.route('/about')
def about():
    return render_template('front_page_about.html')

@views.route('/benefits')
def benefits():
    return render_template('front_page_benefits.html')

@views.route('/contact')
def contact():
    return render_template('front_page_contact.html')


@views.route('/usereventsparticipation')
def eventsparticipation():
    return render_template('user_events_participation.html')

@views.route('/usercommitteeparticipation')
def committeeparticipation():
    return render_template('user_committee_participation.html')

# -- ADMIN SIDE BAR --
@views.route('/admin/members')
def admin_member_management():
    return render_template('admin_member_management.html')

@views.route('/admin/memberships')
def admin_membership_management():
    return render_template('admin_membership_management.html')

@views.route('/admin/billing')
def admin_billing_payment():
    return render_template('admin_billing_payment.html')

@views.route('/admin/events')
def admin_event_management():
    return render_template('admin_event_management.html')

@views.route('/admin/committees')
def admin_committee_dashboard():
    return render_template('admin_committee_dashboard.html')

@views.route('/admin/staff')
def admin_staff_management():
    return render_template('admin_staff_management.html')

# API endpoints to fetch locations data from Supabase
@views.route('/api/regions', methods=['GET'])
def get_regions():
    try:
        response = supabase.table('region').select('*').execute()
        logging.info(f"Supabase response: {response}")  # Log the response for debugging
        
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        
        if response.data is None or not isinstance(response.data, list):
            return jsonify({'error': 'No data found or invalid data format'}), 404
        
        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching regions: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500
@views.route('/api/provinces', methods=['GET'])
def get_provinces():
    region_id = request.args.get('regionid')
    try:
        response = supabase.table('province').select('*').eq('regionid', region_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@views.route('/api/cities', methods=['GET'])
def get_cities():
    province_id = request.args.get('provinceid')
    try:
        response = supabase.table('city').select('*').eq('provinceid', province_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@views.route('/api/barangays', methods=['GET'])  # Match JS call
def get_barangays():
    city_id = request.args.get('cityid')
    try:
        response = supabase.table('barangay').select('*').eq('cityid', city_id).execute()

        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500

        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching barangays for cityid={city_id}: {e}")
        return jsonify({'error': str(e)}), 500

    
@views.route('/api/instregions', methods=['GET'])
def get_instregions():
    try:
        response = supabase.table('region').select('*').execute()
        logging.info(f"Supabase response: {response}")  # Log the response for debugging
        
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        
        if response.data is None or not isinstance(response.data, list):
            return jsonify({'error': 'No data found or invalid data format'}), 404
        
        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching regions: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500
    
@views.route('/api/instprovinces', methods=['GET'])
def get_instprovinces():
    region_id = request.args.get('regionid')
    try:
        response = supabase.table('province').select('*').eq('regionid', region_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@views.route('/api/instcities', methods=['GET'])
def get_instcities():
    province_id = request.args.get('provinceid')
    try:
        response = supabase.table('city').select('*').eq('provinceid', province_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@views.route('/api/instbarangays', methods=['GET'])
def get_instbarangays():
    city_id = request.args.get('cityid')  # ✅ Correct key
    try:
        response = supabase.table('barangay').select('*').eq('cityid', city_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@views.route('/api/schnames', methods=['GET'])
def get_schnames():
    city_id = request.args.get('cityid')
    try:
        response = supabase.table('schname').select('*').eq('cityid', city_id).execute()
        logging.info(f"Supabase response: {response}")  # Log the response for debugging
        
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        
        if response.data is None or not isinstance(response.data, list):
            return jsonify({'error': 'No data found or invalid data format'}), 404
        
        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching regions: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500
    
@views.route('/api/schooltype', methods=['GET'])
def get_school_type():
    school_id = request.args.get('schoolid')
    if not school_id:
        return jsonify({'error': 'schoolid parameter is required'}), 400

    try:
        # 1. Get the typeid from schname
        schname_resp = supabase.table('schname').select('typeid').eq('id', school_id).single().execute()
        typeid = schname_resp.data['typeid']
        if not typeid:
            return jsonify({'error': 'School typeid not found'}), 404

        # 2. Get the school type name from schtype
        schtype_resp = supabase.table('schtype').select('type').eq('id', typeid).single().execute()
        return jsonify({'schooltype': schtype_resp.data['type']}), 200

    except Exception as e:
        logging.error(f"Error fetching school type: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


    

# -- API FOR SCHOOL ADDRESS --
@views.route('/api/schregions', methods=['GET'])
def get_schregions():
    try:
        response = supabase.table('schregion').select('*').execute()
        logging.info(f"Supabase response: {response}")  # Log the response for debugging
        
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        
        if response.data is None or not isinstance(response.data, list):
            return jsonify({'error': 'No data found or invalid data format'}), 404
        
        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching regions: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500
    
@views.route('/api/schprovinces', methods=['GET'])
def get_schprovinces():
    region_id = request.args.get('regionid')
    try:
        response = supabase.table('schprovince').select('*').eq('regionid', region_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@views.route('/api/schcities', methods=['GET'])
def get_schcities():
    province_id = request.args.get('provinceid')
    try:
        response = supabase.table('schcity').select('*').eq('provinceid', province_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -- ADMIN DASHBOARD --
@views.route('/admindashboard')
def admin_dashboard():
    if session.get('user_type') != 'staff':
        return redirect('/')
    return render_template('admin_dashboard.html')

# -- MEMBER DASHBOARD --
@views.route('/userdashboard', methods=['GET'])
def userdashboard():
    if session.get('user_type') != 'member':
        return redirect('/')

    member_id = session.get('member_id')

    # Step 1: Get role from member table
    role_resp = supabase.table('member').select('role').eq('memberid', member_id).maybe_single().execute()
    if not role_resp or not role_resp.data:
        return "Member role not found", 404

    role = role_resp.data['role']

    # Step 2: Depending on role, get full name
    if role == 'individual':
        info_resp = supabase.table('individual').select('firstname, lastname').eq('memberid', member_id).maybe_single().execute()
        if not info_resp or not info_resp.data:
            return "Individual info not found", 404
        data = info_resp.data
        fullname = f"{data['firstname']} {data['lastname']}"

    elif role == 'institution':
        info_resp = supabase.table('institutional').select(
            'representativefirstname, representativemiddlename, representativelastname'
        ).eq('memberid', member_id).maybe_single().execute()
        if not info_resp or not info_resp.data:
            return "Institutional info not found", 404
        data = info_resp.data
        fullname = f"{data['representativefirstname']} {data.get('representativemiddlename') or ''} {data['representativelastname']}".strip()

    else:
        return "Unknown role", 400

    # Step 3: Get membership status
    membership_resp = supabase.table('membershipregistration').select(
        'status, startdate, enddate'
    ).eq('memberid', member_id).eq('status', 'Active').maybe_single().execute()

    if membership_resp and membership_resp.data:
        membership_status = membership_resp.data['status']
        validity_start = membership_resp.data['startdate']
        validity_end = membership_resp.data['enddate']
    else:
        membership_status = "No Active Membership"
        validity_start = None
        validity_end = None

    return render_template(
        'user_dashboard.html',
        fullname=fullname,
        membership_status=membership_status,
        validity_start=validity_start,
        validity_end=validity_end
    )

@views.route('/usermembershipdetails')
def membershipdetails():
    # Get member_id from session
    member_id = session.get('member_id')
    if not member_id:
        return "Unauthorized", 401

    # Check if the member exists in the member table
    member_check_resp = supabase.table('member').select('memberid').eq('memberid', member_id).execute()

    if not member_check_resp.data:
        logging.error("Member check failed: Member not found")
        return "Unauthorized: Member not found", 401

    # Get current active membership
    current_resp = supabase.table('membershipregistration').select(
        'membershipregistrationid, typeid, startdate, enddate, status, membershiptype(name, description, annualfee, benefits)'
    ).eq('memberid', member_id).eq('status', 'Active').execute()

    current_membership = current_resp.data[0] if current_resp.data else None

    # Get full registration history
    history_resp = supabase.table('membershipregistration').select(
        'membershipregistrationid, typeid, startdate, enddate, status, membershiptype(name)'
    ).eq('memberid', member_id).order('startdate', desc=True).execute()

    membership_history = history_resp.data if history_resp.data else []

    # Logging for debugging
    logging.info(f"Current Membership: {current_membership}")
    logging.info(f"Membership History: {membership_history}")

    return render_template(
        'user_membership_details.html',
        current_membership=current_membership,
        membership_history=membership_history
    )

@views.route('/userprofile', methods=['GET', 'POST'])
def profile():
    if session.get('user_type') != 'member':
        print("User  not member. Redirecting.")
        return redirect('/')

    member_id = session.get('member_id')
    print("Session Member ID:", member_id)

    if request.method == 'POST':
        # Handle the profile update logic here
        data = request.json
        return update_profile(data, member_id)  # Call the update function

    # Fetch member data for GET request
    member_resp = supabase.table('member').select(
        'streetaddress, email, emergencycontactnumber'
    ).eq('memberid', member_id).execute()
    member = member_resp.data[0] if member_resp.data else {}

    # Fetch individual data
    individual_resp = supabase.table('individual').select(
        'firstname, lastname, phone'
    ).eq('memberid', member_id).execute()
    individual = individual_resp.data[0] if individual_resp.data else {}

    # Compose full name
    fullname = f"{individual.get('firstname', '')} {individual.get('lastname', '')}".strip()

    # Render profile template
    return render_template(
        'user_profile.html',
        fullname=fullname,
        email=member.get('email', ''),
        phone=individual.get('phone', ''),
        streetaddress=member.get('streetaddress', ''),
        emergency_contact=member.get('emergencycontactnumber', '')
    )

def update_profile(data, member_id):
    if session.get('user_type') != 'member':
        return jsonify({'message': 'Unauthorized'}), 403

    # Extract profile info
    phone = data.get('phone')
    streetaddress = data.get('streetaddress')  # Ensure this is correctly extracted
    emergency_contact = data.get('emergencycontactnumber')

    # Update member table
    member_update_response = supabase.table('member').update({
        'streetaddress': streetaddress,  # Ensure this is being updated
        'emergencycontactnumber': emergency_contact
    }).eq('memberid', member_id).execute()

    # Check for errors in the response
    if member_update_response.get('error'):
        return jsonify({'message': 'Failed to update member: ' + str(member_update_response['error'])}), 500

    # Update individual table
    individual_update_response = supabase.table('individual').update({
        'phone': phone,
    }).eq('memberid', member_id).execute()

    # Check for errors in the response
    if individual_update_response.get('error'):
        return jsonify({'message': 'Failed to update individual: ' + str(individual_update_response['error'])}), 500

    # Handle password change if provided
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if current_password and new_password:
        member_resp = supabase.table('member').select('password').eq('memberid', member_id).execute()
        if not member_resp.data:
            return jsonify({'message': 'Member not found'}), 404

        hashed = member_resp.data[0]['password']
        if not check_password_hash(hashed, current_password):
            return jsonify({'message': 'Current password is incorrect'}), 400

        new_hashed = generate_password_hash(new_password)
        password_update_response = supabase.table('member').update({'password': new_hashed}).eq('memberid', member_id).execute()

        # Check for errors in the response
        if password_update_response.get('error'):
            return jsonify({'message': 'Failed to update password: ' + str(password_update_response['error'])}), 500

    return jsonify({'message': 'Profile updated successfully'})





@views.route('/userbillingpayment')
def billingpayment():
    if session.get('user_type') != 'member':
        return redirect('/')
    return render_template('user_billing_payment.html')