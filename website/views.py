from flask import Blueprint, jsonify, render_template, abort, request, session, redirect
from . import models
from .supabase_client import supabase
from datetime import datetime
import logging

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

@views.route('/userprofile')
def profile():
    return render_template('user_profile.html')

# @views.route('/usermembershipdetails')
# def membershipdetails():
#     return render_template('user_membership_details.html')

@views.route('/userbillingpayment')
def billingpayment():
    return render_template('user_billing_payment.html')

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
    
@views.route('/api/barangays', methods=['GET'])
def get_barangays():
    city_id = request.args.get('cityid')
    try:
        response = supabase.table('barangay').select('*').eq('cityid', city_id).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

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
    return render_template('user_dashboard.html', member_id=member_id)

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


# --- MEMBER ROUTES ---
@views.route('/members', methods=['GET'])
def list_members():
    member, error = models.get_all_members(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(member), 200

@views.route('/members/<int:memberid>', methods=['GET'])
def get_member(memberid):
    member, error = models.get_member_by_id(supabase, memberid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(member), 200

@views.route('/members', methods=['POST'])
def create_member():
    data = request.json or {}
    validate_required_fields(data, ['firstname', 'lastname', 'emailaddress'])

    if 'dateofbirth' in data:
        converted = iso_date(data['dateofbirth'])
        if not converted:
            return jsonify({"error": "DateOfBirth must be YYYY-MM-DD"})
        data['dateofbirth'] = converted

    if 'joindate' not in data:
        data['joindate'] = datetime.utcnow().isoformat()

    
    new_member, error = models.create_member(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_member), 201

@views.route('/members/<int:memberid>', methods=['PUT'])
def update_member(memberid):
    data = request.json or {}

    if 'dateofbirth' in data:
        converted = iso_date(data['dateofbirth'])
        if not converted:
            return jsonify({"error": "DateOfBirth must be YYYY-MM-DD"})
        data['dateofbirth'] = converted

    updated_member, error = models.update_member(supabase, memberid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_member), 200

@views.route('/members/<int:memberid>', methods=['DELETE'])
def delete_member(memberid):
    success, error = models.delete_member(supabase, memberid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete member"}), 400
    return jsonify({"message": "Member deleted"}), 200

# --- MEMBERSHIPTYPE ROUTES ---
@views.route('/membership_types/<int:typeid>', methods=['GET'])
def get_membership_type(typeid):
    mt, error = models.get_membership_type_by_id(supabase, typeid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(mt), 200

@views.route('/membership_types', methods=['POST'])
def create_membership_type():
    data = request.json or {}
    validate_required_fields(data, ['Name'])
    mt, error = models.create_membership_type(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(mt), 201

@views.route('/membership_types/<int:typeid>', methods=['PUT'])
def update_membership_type(typeid):
    data = request.json or {}
    mt, error = models.update_membership_type(supabase, typeid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(mt), 200

@views.route('/membership_types/<int:typeid>', methods=['DELETE'])
def delete_membership_type(typeid):
    success, error = models.delete_membership_type(supabase, typeid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete membership type"}), 400
    return jsonify({"message": "Membership type deleted"}), 200

# --- MEMBERSHIP REGISTRATION ROUTES ---
@views.route('/membership_registrations', methods=['GET'])
def list_membership_registrations():
    data, error = models.get_all_membership_registrations(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/membership_registrations/<int:regid>', methods=['GET'])
def get_membership_registration(regid):
    data, error = models.get_membership_registration_by_id(supabase, regid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200

@views.route('/membership_registrations', methods=['POST'])
def create_membership_registration():
    data = request.json or {}
    validate_required_fields(data, ['MemberID', 'TypeID', 'StartDate', 'EndDate'])
    new_reg, error = models.create_membership_registration(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_reg), 201

@views.route('/membership_registrations/<int:regid>', methods=['PUT'])
def update_membership_registration(regid):
    data = request.json or {}
    updated_reg, error = models.update_membership_registration(supabase, regid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_reg), 200

@views.route('/membership_registrations/<int:regid>', methods=['DELETE'])
def delete_membership_registration(regid):
    success, error = models.delete_membership_registration(supabase, regid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete registration"}), 400
    return jsonify({"message": "Registration deleted"}), 200

# --- PAYER ROUTES ---
@views.route('/payers', methods=['GET'])
def list_payers():
    payers, error = models.get_all_payers(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(payers), 200

@views.route('/payers/<int:payerid>', methods=['GET'])
def get_payer(payerid):
    payer, error = models.get_payer_by_id(supabase, payerid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(payer), 200

@views.route('/payers', methods=['POST'])
def create_payer():
    data = request.json or {}
    validate_required_fields(data, ['Name', 'Type'])
    payer, error = models.create_payer(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(payer), 201

@views.route('/payers/<int:payerid>', methods=['PUT'])
def update_payer(payerid):
    data = request.json or {}
    payer, error = models.update_payer(supabase, payerid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(payer), 200

@views.route('/payers/<int:payerid>', methods=['DELETE'])
def delete_payer(payerid):
    success, error = models.delete_payer(supabase, payerid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete payer"}), 400
    return jsonify({"message": "Payer deleted"}), 200

# --- BILLING ROUTES ---
@views.route('/billing', methods=['GET'])
def list_billing():
    data, error = models.get_all_billing(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/billing/<int:billingid>', methods=['GET'])
def get_billing(billingid):
    data, error = models.get_billing_by_id(supabase, billingid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200

@views.route('/billing', methods=['POST'])
def create_billing():
    data = request.json or {}
    validate_required_fields(data, ['MembershipID', 'PayerID', 'BillDate', 'AmountDue', 'DueDate', 'Status']) # notsure
    new_bill, error = models.create_billing(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_bill), 201

@views.route('/billing/<int:billingid>', methods=['PUT'])
def update_billing(billingid):
    data = request.json or {}
    updated_bill, error = models.update_billing(supabase, billingid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_bill), 200

@views.route('/billing/<int:billingid>', methods=['DELETE'])
def delete_billing(billingid):
    success, error = models.delete_billing(supabase, billingid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete billing"}), 400
    return jsonify({"message": "Billing deleted"}), 200

# --- PAYMENTS ROUTE ---
@views.route('/payments', methods=['GET'])
def list_payments():
    data, error = models.get_all_payments(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/payments/<int:paymentid>', methods=['GET'])
def get_payment(paymentid):
    data, error = models.get_payment_by_id(supabase, paymentid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200

@views.route('/payments', methods=['POST'])
def create_payment():
    data = request.json or {}
    validate_required_fields(data, ['BillingID', 'AmountPaid', 'PaymentDate', 'Method', 'Status'])
    new_payment, error = models.create_payment(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_payment), 201

@views.route('/payments/<int:paymentid>', methods=['PUT'])
def update_payment(paymentid):
    data = request.json or {}
    updated_payment, error = models.update_payment(supabase, paymentid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_payment), 200

@views.route('/payments/<int:paymentid>', methods=['DELETE'])
def delete_payment(paymentid):
    success, error = models.delete_payment(supabase, paymentid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete payment"}), 400
    return jsonify({"message": "Payment deleted"}), 200

# --- COMMITTEES ROUTES ---
@views.route('/committees', methods=['GET'])
def list_committees():
    data, error = models.get_all_committees(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/committees/<int:committeeid>', methods=['GET'])
def get_committee(committeeid):
    data, error = models.get_committee_by_id(supabase, committeeid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200

@views.route('/committees', methods=['POST'])
def create_committee():
    data = request.json or {}
    validate_required_fields(data, ['Name'])
    new_committee, error = models.create_committee(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_committee), 201

@views.route('/committees/<int:committeeid>', methods=['PUT'])
def update_committee(committeeid):
    data = request.json or {}
    updated_committee, error = models.update_committee(supabase, committeeid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_committee), 200

@views.route('/committees/<int:committeeid>', methods=['DELETE'])
def delete_committee(committeeid):
    success, error = models.delete_committee(supabase, committeeid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete committee"}), 400
    return jsonify({"message": "Committee deleted"}), 200

# --- COMMITTEE MEMBERS ROUTES ---
@views.route('/committee_members', methods=['GET'])
def list_committee_members():
    data, error = models.get_all_committee_members(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/committee_members/<int:committeeid>/<int:memberid>', methods=['GET'])
def get_committee_member(committeeid, memberid):
    data, error = models.get_committee_member(supabase, committeeid, memberid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200

@views.route('/committee_members', methods=['POST'])
def create_committee_member():
    data = request.json or {}
    validate_required_fields(data, ['CommitteeID','MemberID','Role','ApplicationDate','Status'])
    new_cm, error = models.create_committee_member(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_cm), 201

@views.route('/committee_members/<int:committeeid>/<int:memberid>', methods=['PUT'])
def update_committee_member(committeeid, memberid):
    data = request.json or {}
    updated_cm, error = models.update_committee_member(supabase, committeeid, memberid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_cm), 200

@views.route('/committee_members/<int:committeeid>/<int:memberid>', methods=['DELETE'])
def delete_committee_member(committeeid, memberid):
    success, error = models.delete_committee_member(supabase, committeeid, memberid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete committee member"}), 400
    return jsonify({"message": "Committee member deleted"}), 200

# --- EVENTS ROUTES ---
@views.route('/events', methods=['GET'])
def list_events():
    data, error = models.get_all_events(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/events/<int:eventid>', methods=['GET'])
def get_event(eventid):
    data, error = models.get_event_by_id(supabase, eventid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200

@views.route('/events', methods=['POST'])
def create_event():
    data = request.json or {}
    validate_required_fields(data, ['Name', 'EventDate'])
    new_event, error = models.create_event(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_event), 201

@views.route('/events/<int:eventid>', methods=['PUT'])
def update_event(eventid):
    data = request.json or {}
    updated_event, error = models.update_event(supabase, eventid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_event), 200

@views.route('/events/<int:eventid>', methods=['DELETE'])
def delete_event(eventid):
    success, error = models.delete_event(supabase, eventid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete event"}), 400
    return jsonify({"message": "Event deleted"}), 200

# --- EVENT REGISTRATION ROUTES ---
@views.route('/event_registrations', methods=['GET'])
def list_event_registrations():
    data, error = models.get_all_event_registrations(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/event_registrations/<int:registrationid>', methods=['GET'])
def get_event_registration(registrationid):
    data, error = models.get_event_registration_by_id(supabase, registrationid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200

@views.route('/event_registrations', methods=['POST'])
def create_event_registration():
    data = request.json or {}
    validate_required_fields(data, ['EventID', 'MemberID', 'RegistrationDate', 'Status'])
    new_ereg, error = models.create_event_registration(supabase, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_ereg), 201

@views.route('/event_registrations/<int:registrationid>', methods=['PUT'])
def update_event_registration(registrationid):
    data = request.json or {}
    updated_ereg, error = models.update_event_registration(supabase, registrationid, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(updated_ereg), 200

@views.route('/event_registrations/<int:registrationid>', methods=['DELETE'])
def delete_event_registration(registrationid):
    success, error = models.delete_event_registration(supabase, registrationid)
    if error or not success:
        return jsonify({"error": error or "Failed to delete event registration"}), 400
    return jsonify({"message": "Event registration deleted"}), 200

# --- STAFF ROUTES ----
@views.route('/staff', methods=['GET'])
def list_staff():
    data, error = models.get_all_staff(supabase)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data), 200

@views.route('/staff/<int:staffid>', methods=['GET'])
def get_staff(staffid):
    data, error = models.get_staff_by_id(supabase, staffid)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data), 200