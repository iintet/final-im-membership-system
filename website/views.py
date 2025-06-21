from flask import Blueprint, jsonify, render_template, abort, request, session, redirect, url_for
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

# -- REGISTRATION --
@views.route('/register/payment', methods=['GET'])
def register_payment():
    return render_template('registration_payment.html')

@views.route('/register/uploadpayment', methods=['GET'])
def register_upload_payment():
    return render_template('registration_upload_payment.html')

@views.route('/auth/login', methods=['GET'])
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

# -- ORGANIZATION DROPDOWN
@views.route('/api/organizations', methods=['GET'])
def get_organizations():
    try:
        response = supabase.table('organization').select('*').execute()
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
     # Total Members
    total_members_resp = supabase.table("member").select("*", count="exact").execute()
    total_members = total_members_resp.count or 0

    # Active Memberships (status = 'Active')
    active_memberships_resp = supabase.table("membershipregistration").select("*", count="exact").eq("status", "Active").execute()
    active_memberships = active_memberships_resp.count or 0

    # Upcoming Events (eventdate >= today)
    from datetime import date
    today = str(date.today())
    upcoming_events_resp = supabase.table("event").select("*", count="exact").gte("eventdate", today).execute()
    upcoming_events = upcoming_events_resp.count or 0

    return render_template("admin_dashboard.html",
                           total_members=total_members,
                           active_memberships=active_memberships,
                           upcoming_events=upcoming_events)

# -- MEMBER MANAGEMENT --
@views.route('/admin/member-management', methods=['GET'])
def admin_member_management():
    search = request.args.get('query', '').strip().lower()

    # Get all members
    member_data = supabase.table("member").select("*").execute().data or []
    individual_data = supabase.table("individual").select("*").execute().data or []
    institutional_data = supabase.table("institutional").select("*").execute().data or []
    membership_data = supabase.table("membershipregistration").select("*").execute().data or []
    membership_types = supabase.table("membershiptype").select("*").execute().data or []

    enriched_members = []

    for m in member_data:
        member = m.copy()

        full_name = ""
        role = member.get('role', '')
        email = member.get('email', '')
        membership_type = 'N/A'
        membership_status = 'N/A'

        if member['role'] == 'individual':
            info = next((i for i in individual_data if i['memberid'] == member['memberid']), {})
            member.update(info)
            full_name = f"{info.get('firstname', '')} {info.get('middlename', '')} {info.get('lastname', '')}"
        else:
            info = next((i for i in institutional_data if i['memberid'] == member['memberid']), {})
            member.update(info)
            full_name = f"{info.get('representativefirstname', '')} {info.get('representativelastname', '')}"

        membership = next((m for m in membership_data if m['memberid'] == member['memberid']), None)
        if membership:
            typeid = membership.get('typeid')
            type_info = next((t for t in membership_types if t['typeid'] == typeid), {})
            membership_type = type_info.get('name', 'N/A')
            membership_status = membership.get('status', 'N/A')
            
        # Apply search filter
        if search and search not in full_name.lower() and search not in member.get("email", "").lower():
            continue

        enriched_members.append({
            'fullname': full_name,
            'email': email,
            'role': role.title(),
            'membershiptype': membership_type,
            'membershipstatus': membership_status,
            'memberid': member['memberid'],
        })

    return render_template('admin_member_management.html', members=enriched_members)

@views.route('/admin/member/view/<memberid>')
def admin_member_view(memberid):
    member = supabase.table("member").select("*").eq("memberid", memberid).execute().data
    if not member:
        return "Member not found", 404
    member = member[0]

    # Fetch individual or institutional details
    if member['role'] == 'individual':
        detail = supabase.table("individual").select("*").eq("memberid", memberid).execute().data
        detail = detail[0] if detail else {}
        full_name = f"{detail.get('firstname', '')} {detail.get('middlename', '')} {detail.get('lastname', '')}"
        phone = detail.get("phone", "")
    else:
        detail = supabase.table("institutional").select("*").eq("memberid", memberid).execute().data
        detail = detail[0] if detail else {}
        full_name = f"{detail.get('representativefirstname', '')} {detail.get('representativemiddlename', '')} {detail.get('representativelastname', '')}"
        phone = detail.get("representativecontactnumber", "")

    # Fetch membership info
    membership = supabase.table("membershipregistration").select("*").eq("memberid", memberid).execute().data
    membership = membership[0] if membership else {}

    # Get membership type name
    membership_type = ""
    if membership:
        type_data = supabase.table("membershiptype").select("name").eq("typeid", membership["typeid"]).execute().data
        if type_data:
            membership_type = type_data[0]["name"]

    return render_template(
        'admin_member_management_view.html',
        name=full_name,
        email=member['email'],
        phone=phone,
        status=membership.get('status', 'N/A'),
        registration_date=membership.get('startdate', 'N/A'),
        membership_type=membership_type,
        additional_notes="Approved by admin after verification."  # you can customize this
    )

@views.route('/admin/member/edit/<memberid>', methods=['GET', 'POST'])
def admin_member_edit(memberid):
    member_data = supabase.table("member").select("*").eq("memberid", memberid).execute().data
    if not member_data:
        return "Member not found", 404
    member = member_data[0]

    # Role-based details
    if member["role"] == "individual":
        detail_data = supabase.table("individual").select("*").eq("memberid", memberid).execute().data
        detail = detail_data[0] if detail_data else {}
        first_name = detail.get("firstname", "")
        last_name = detail.get("lastname", "")
        phone = detail.get("phone", "")
    else:
        detail_data = supabase.table("institutional").select("*").eq("memberid", memberid).execute().data
        detail = detail_data[0] if detail_data else {}
        first_name = detail.get("representativefirstname", "")
        last_name = detail.get("representativelastname", "")
        phone = detail.get("representativecontactnumber", "")

    # Membership status
    membership_data = supabase.table("membershipregistration").select("*").eq("memberid", memberid).execute().data
    status = membership_data[0]["status"] if membership_data else "Active"

    # Handle form POST
    if request.method == "POST":
        email = request.form.get("email")
        phone = request.form.get("phone")
        fname = request.form.get("first-name")
        lname = request.form.get("last-name")
        new_status = request.form.get("membership-status")

        # Update member email
        supabase.table("member").update({"email": email}).eq("memberid", memberid).execute()

        # Update individual/institutional record
        if member["role"] == "individual":
            supabase.table("individual").update({
                "firstname": fname,
                "lastname": lname,
                "phone": phone
            }).eq("memberid", memberid).execute()
        else:
            supabase.table("institutional").update({
                "representativefirstname": fname,
                "representativelastname": lname,
                "representativecontactnumber": phone
            }).eq("memberid", memberid).execute()

        # Update membership status
        if membership_data:
            supabase.table("membershipregistration").update({
                "status": new_status
            }).eq("memberid", memberid).execute()

        return redirect(url_for('views.admin_member_management'))

    return render_template(
        'admin_member_management_edit.html',
        memberid=memberid,
        email=member["email"],
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        status=status
    )

# -- EVENT MANAGEMENT -- 
@views.route('/admin/events')
def admin_event_management():
    return render_template('admin_event_management.html')

@views.route('/admin/events/view')
def admin_event_view():
    try:
        # Get filter params from query
        from_date_str = request.args.get('from_date')
        to_date_str = request.args.get('to_date')
        status_filter = request.args.get('status')
        capacity_sort = request.args.get('capacity_sort')  # 'asc' or 'desc'

        events_result = supabase.table("event").select("*").execute()
        events = events_result.data

        enriched_events = []
        for event in events:
            eventid = event["eventid"]
            name = event["name"]
            location = event["location"]
            capacity = event["capacity"]

            # Parse date
            eventdate = datetime.strptime(event["eventdate"], "%Y-%m-%d").date()
            today = datetime.today().date()
            status = "Upcoming" if eventdate >= today else "Completed"

            # Apply date filter
            if from_date_str:
                from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
                if eventdate < from_date:
                    continue
            if to_date_str:
                to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()
                if eventdate > to_date:
                    continue

            # Apply status filter
            if status_filter and status_filter != "All" and status != status_filter:
                continue

            # Count registrations
            reg_result = supabase.table("eventregistration").select("registrationid").eq("eventid", eventid).execute()
            registered = len(reg_result.data)
            available = max(capacity - registered, 0)

            enriched_events.append({
                "name": name,
                "eventdate": eventdate.strftime("%B %d, %Y"),
                "raw_date": eventdate,  # for sorting
                "location": location,
                "status": status,
                "capacity": capacity,
                "registered": registered,
                "available": available
            })

        # Sort by capacity
        if capacity_sort == "asc":
            enriched_events.sort(key=lambda x: x["capacity"])
        elif capacity_sort == "desc":
            enriched_events.sort(key=lambda x: x["capacity"], reverse=True)

        return render_template("admin_event_view.html", events=enriched_events,
                               from_date=from_date_str, to_date=to_date_str,
                               status_filter=status_filter or "All",
                               capacity_sort=capacity_sort or "")

    except Exception as e:
        print("Error fetching events:", e)
        return render_template("admin_event_view.html", events=[])

@views.route('/admin/events/manage')
def admin_event_manage():
    response = supabase.table("event").select("*").order("eventdate", desc=False).execute()
    events = response.data if response.data else []
    return render_template('admin_event_manage.html', events=events)

@views.route('/admin/event/registrations')
def admin_event_registrations():
    try:
        # Step 1: Get all event registrations ordered by date (latest first)
        result = supabase.table("eventregistration").select(
            "registrationid, registrationdate, status, memberid, eventid"
        ).order("registrationdate", desc=True).execute()

        registrations = result.data

        enriched_registrations = []
        for reg in registrations:
            memberid = reg["memberid"]
            # Get member base info (to know role)
            member_result = supabase.table("member").select("role").eq("memberid", memberid).execute().data
            if not member_result:
                continue
            role = member_result[0]["role"]

            # Get name and contact info
            if role == "individual":
                detail_result = supabase.table("individual").select(
                    "firstname, middlename, lastname"
                ).eq("memberid", memberid).execute().data
                if detail_result:
                    d = detail_result[0]
                    full_name = f"{d.get('firstname', '')} {d.get('middlename', '')} {d.get('lastname', '')}".strip()
                else:
                    full_name = "Unknown Individual"
            else:
                detail_result = supabase.table("institutional").select(
                    "representativefirstname, representativemiddlename, representativelastname"
                ).eq("memberid", memberid).execute().data
                if detail_result:
                    d = detail_result[0]
                    full_name = f"{d.get('representativefirstname', '')} {d.get('representativemiddlename', '')} {d.get('representativelastname', '')}".strip()
                else:
                    full_name = "Unknown Institution"

            # Get event name
            event_result = supabase.table("event").select("name").eq("eventid", reg["eventid"]).execute().data
            event_name = event_result[0]["name"] if event_result else "Unknown Event"

            enriched_registrations.append({
                "registrationid": reg["registrationid"],
                "registrationdate": reg["registrationdate"],
                "status": reg["status"],
                "member_name": full_name,
                "event_name": event_name
            })

        return render_template("admin_event_registrations.html", registrations=enriched_registrations)

    except Exception as e:
        print("Error loading event registrations:", e)
        return render_template("admin_event_registrations.html", registrations=[])

# -- MEMBERSHIP MANAGEMENT --
@views.route('/admin/memberships')
def admin_membership_management():
    return render_template('admin_membership_management.html')

@views.route('/admin/membership/edit')
def admin_membership_edit():
    membership_types = supabase.table('membershiptype').select('*').execute().data or []
    return render_template('admin_membership_management_edit_type.html', membership_types=membership_types)

@views.route('/admin/membership/history', methods=['GET'])
def admin_membership_registration_history():
    # Get filter values from query string
    status_filter = request.args.get('status', '').lower()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Fetch all membership registrations
    registration_data = supabase.table("membershipregistration").select("*").execute().data

    # Fetch member and membership type data
    members = supabase.table("member").select("memberid, role").execute().data
    individuals = supabase.table("individual").select("memberid, firstname, middlename, lastname").execute().data
    institutions = supabase.table("institutional").select("memberid, representativefirstname, representativemiddlename, representativelastname").execute().data
    types = supabase.table("membershiptype").select("typeid, name").execute().data

    enriched = []
    for reg in registration_data:
        reg_status = reg.get("status", "").lower()
        date = reg.get("startdate")
        end = reg.get("enddate")

        if not date:
            continue

        # Filter by status
        if status_filter and status_filter != reg_status:
            continue

        # Filter by date range
        try:
            reg_date = datetime.strptime(date, '%Y-%m-%d').date()
            if start_date:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                if reg_date < start:
                    continue
            if end_date:
                end_d = datetime.strptime(end_date, '%Y-%m-%d').date()
                if reg_date > end_d:
                    continue
        except ValueError:
            continue

        # Get name
        member_id = reg.get("memberid")
        role = next((m['role'] for m in members if m['memberid'] == member_id), '')

        if role == 'individual':
            info = next((i for i in individuals if i['memberid'] == member_id), {})
            name = f"{info.get('firstname', '')} {info.get('middlename', '')} {info.get('lastname', '')}".strip()
        elif role == 'institution':
            info = next((i for i in institutions if i['memberid'] == member_id), {})
            name = f"{info.get('representativefirstname', '')} {info.get('representativemiddlename', '')} {info.get('representativelastname', '')}".strip()
        else:
            name = "Unknown"

        # Get membership type name
        type_name = next((t['name'] for t in types if t['typeid'] == reg.get("typeid")), "")

        enriched.append({
            "name": name,
            "registration_date": date,
            "end_date": end,
            "status": reg.get("status"),
            "type": type_name
        })

    # Sort by registration date (descending)
    enriched.sort(key=lambda x: x['registration_date'], reverse=True)

    return render_template("admin_membership_registration_history.html", registrations=enriched)

# -- ADMIN BILLING --
@views.route('/admin/billing')
def admin_billing_payment():
    return render_template('admin_billing_payment.html')

@views.route('/admin/billing/create', methods=['GET', 'POST'])
def admin_create_billing():
    return render_template('admin_create_bill.html')

@views.route('/admin/payment/record', methods=['GET'])
def admin_payment_record():
    return render_template('admin_record_payment.html')

# -- ADMIN COMMITTEE MANAGEMENT --
@views.route('/admin/committees')
def admin_committee_dashboard():
    return render_template('admin_committee_dashboard.html')

@views.route('/admin/committees/view')
def admin_committee_view():
        return render_template('admin_committee_view.html')

@views.route('/admin/committees/manage')
def admin_committee_manage():
    return render_template('admin_committee_manage_members.html')

@views.route('/admin/committees/status')
def admin_committee_status():
    return render_template('admin_committee_application_status.html')

@views.route('/admin/committees/roles')
def admin_committee_roles():
    return render_template('admin_committee_role_assignment.html')

# -- STAFF MANAGEMENT --

@views.route('/admin/staff')
def admin_staff_management():
    return render_template('admin_staff_management.html')

@views.route('/admin/staff/manage')
def admin_staff_manage():
    return render_template('admIn_staff_manage_account.html')

@views.route('/admin/staff/roles')
def admin_staff_roles():
    return render_template('admin_staff_assign_roles.html')

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
        return redirect('/')

    member_id = session.get('member_id')
    if not member_id:
        return redirect('/')

    try:
        if request.method == 'POST':
            data = request.get_json()
            print("Payload received:", data)
            return update_profile(data, member_id)

        # Fetch member info
        member_resp = supabase.table('member').select(
            'streetaddress, email, emergencycontactnumber, emergencycontactname, region, province, city, barangay'
        ).eq('memberid', member_id).execute()
        member = member_resp.data[0] if member_resp.data else {}

        # Fetch individual info
        individual_resp = supabase.table('individual').select(
            'firstname, lastname, phone'
        ).eq('memberid', member_id).execute()
        individual = individual_resp.data[0] if individual_resp.data else {}

        # Fetch name equivalents for location fields
        region_resp = supabase.table('region').select('regionname').eq('regionid', member.get('region')).single().execute()
        province_resp = supabase.table('province').select('provincename').eq('provinceid', member.get('province')).single().execute()
        city_resp = supabase.table('city').select('cityname').eq('cityid', member.get('city')).single().execute()
        barangay_resp = supabase.table('barangay').select('barangayname').eq('barangayid', member.get('barangay')).single().execute()

        fullname = f"{individual.get('firstname', '')} {individual.get('lastname', '')}".strip()

        return render_template(
            'user_profile.html',
            fullname=fullname,
            email=member.get('email', ''),
            phone=individual.get('phone', ''),
            streetaddress=member.get('streetaddress', ''),
            emergency_contact=member.get('emergencycontactnumber', ''),
            emergency_contact_name=member.get('emergencycontactname', ''),
            region_name=region_resp.data['regionname'] if region_resp.data else '',
            province_name=province_resp.data['provincename'] if province_resp.data else '',
            city_name=city_resp.data['cityname'] if city_resp.data else '',
            barangay_name=barangay_resp.data['barangayname'] if barangay_resp.data else '',
            region_id=member.get('region'),
            province_id=member.get('province'),
            city_id=member.get('city'),
            barangay_id=member.get('barangay'),

        )
    except Exception as e:
        print("Error rendering profile:", e)
        return jsonify({'message': 'Internal server error'}), 500

def update_profile(data, member_id):
    if session.get('user_type') != 'member':
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        # Extract allowed fields from the frontend
        phone = data.get('phone')
        streetaddress = data.get('streetaddress')
        emergency_contact = data.get('emergencycontactnumber')
        emergency_contact_name = data.get('emergencycontactname')

        region = data.get('region')
        province = data.get('province')
        city = data.get('city')
        barangay = data.get('barangay')

        # Defensive check: ignore any forbidden field edits
        blocked_fields = ['firstname', 'lastname', 'gender', 'dateofbirth']
        for field in blocked_fields:
            if field in data:
                print(f"Ignoring restricted update attempt: {field}")

        # Update member table
        member_update = {
            'streetaddress': streetaddress,
            'emergencycontactnumber': emergency_contact,
            'emergencycontactname': emergency_contact_name,
            'region': int(region) if region else None,
            'province': int(province) if province else None,
            'city': int(city) if city else None,
            'barangay': int(barangay) if barangay else None
        }

        supabase.table('member').update(member_update).eq('memberid', member_id).execute()

        # Update individual phone separately
        supabase.table('individual').update({
            'phone': phone
        }).eq('memberid', member_id).execute()

        # Password update if provided
        if data.get('current_password') and data.get('new_password'):
            member_resp = supabase.table('member').select('password').eq('memberid', member_id).execute()
            if not member_resp.data:
                return jsonify({'message': 'Member not found'}), 404

            hashed = member_resp.data[0]['password']
            if not check_password_hash(hashed, data['current_password']):
                return jsonify({'message': 'Current password is incorrect'}), 400

            new_hashed = generate_password_hash(data['new_password'])
            supabase.table('member').update({'password': new_hashed}).eq('memberid', member_id).execute()

            print("Payload received:", data)

        return jsonify({'message': 'Profile updated successfully'})
    
    except Exception as e:
        print("Profile update failed:", e)
        return jsonify({'message': 'Server error while updating profile'}), 500

@views.route('/userbillingpayment')
def billingpayment():
    if session.get('user_type') != 'member':
        return redirect('/')
    return render_template('user_billing_payment.html')

@views.route('/api/events', methods=['POST'])
def create_event():
    if session.get('user_type') != 'staff':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    required_fields = ['eventname', 'eventdate', 'location', 'description']
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        response = supabase.table('event').insert({
            'eventname': data['eventname'],
            'eventdate': data['eventdate'],
            'location': data['location'],
            'description': data['description']
        }).execute()

        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500

        return jsonify({'message': 'Event created successfully', 'event': response.data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500