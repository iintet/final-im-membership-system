from flask import Blueprint, jsonify, render_template, abort, request, session, redirect, url_for, flash
from . import models
from werkzeug.utils import secure_filename
from .supabase_client import supabase
from datetime import datetime, date
import logging, os
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
    
    if not city_id or not city_id.isdigit():
        return jsonify({'error': 'Invalid or missing cityid'}), 400

    try:
        response = supabase.table('schname').select('*').eq('cityid', int(city_id)).execute()
        if hasattr(response, 'error') and response.error:
            return jsonify({'error': str(response.error)}), 500

        if response.data is None or not isinstance(response.data, list):
            return jsonify({'error': 'No data found or invalid data format'}), 404

        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching school names: {str(e)}")
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
@views.route('/staff/dashboard')
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
    filter_role = request.args.get('role', '').strip().lower()
    filter_membership_type = request.args.get('membershiptype', '').strip().lower()
    filter_status = request.args.get('status', '').strip().lower()

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
        if search and search not in full_name.lower() and search not in email.lower():
            continue
        if filter_role and role.lower() != filter_role:
            continue
        if filter_membership_type and membership_type.lower() != filter_membership_type:
            continue
        if filter_status and membership_status.lower() != filter_status:
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
    date_filter = request.args.get('date_filter')
    capacity_filter = request.args.get('capacity_filter')

    query = (
        supabase.table("event")
        .select("""
            eventid,
            name,
            eventdate,
            location,
            capacity,
            fee,
            staffid,
            staff (
                firstname,
                lastname
            )
        """)
    )

    # Apply filters if any
    if date_filter:
        query = query.gte("eventdate", date_filter)

    if capacity_filter:
        query = query.gte("capacity", int(capacity_filter))

    # Sort + execute
    events_data = query.order("eventdate", desc=False).execute().data

    # Get staff list
    staff_list = supabase.table("staff").select("staffid, firstname, lastname").execute().data

    return render_template(
        "admin_event_manage.html",
        events=events_data,
        staff_list=staff_list,
        date_filter=date_filter,
        capacity_filter=capacity_filter
    )

@views.route('/admin/event/add', methods=['POST'])
def add_event():
    name = request.form.get("name")
    date = request.form.get("date")
    location = request.form.get("location")
    capacity = int(request.form.get("capacity"))
    fee = float(request.form.get("fee"))
    staff_id = request.form.get("staff_id")

    if name and date and location and capacity and fee and staff_id:
        supabase.table("event").insert({
            "name": name,
            "eventdate": date,
            "location": location,
            "capacity": capacity,
            "fee": fee,
            "staffid": staff_id
        }).execute()

    return redirect(url_for('views.admin_event_manage'))

@views.route('/admin/event/delete/<int:eventid>', methods=['POST'])
def delete_event(eventid):
    supabase.table("event").delete().eq("eventid", eventid).execute()
    return redirect(url_for('views.admin_event_management'))

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
    due_date = request.args.get('due_date')
    status = request.args.get('status', 'all')

    query = supabase.table("billing").select("""
        billingid,
        billdate,
        duedate,
        amountdue,
        status,
        billtype,
        member:memberid (
            individual (
                firstname,
                lastname
            )
        )
    """)

    if due_date:
        query = query.gte("duedate", due_date)
    if status and status != 'all':
        query = query.eq("status", status)

    billing_data = query.execute().data

    return render_template(
        "admin_billing_payment.html",
        billing=billing_data,
        due_date=due_date,
        status=status
    )

@views.route('/admin/billing/create', methods=['GET', 'POST'])
def admin_create_billing():
    if request.method == 'POST':
        member_name = request.form.get('member_name').strip()
        bill_type = request.form.get('bill_type')
        bill_date = request.form.get('bill_date')
        due_date = request.form.get('due_date')
        status = request.form.get('status')
        amountdue = request.form.get('amountdue')

        # Split the name for matching (basic approach)
        name_parts = member_name.split()
        firstname = name_parts[0]
        lastname = name_parts[-1] if len(name_parts) > 1 else ''

        # Search for individual
        member_query = supabase.table("member").select("""
            memberid,
            individual (
                firstname,
                lastname
            )
        """).execute().data

        matched_member = next(
            (
                m for m in member_query
                if m.get("individual") and
                m["individual"]["firstname"].lower() == firstname.lower() and
                m["individual"]["lastname"].lower() == lastname.lower()
            ),
            None
        )

        if not matched_member:
            return "Member not found", 404

        member_id = matched_member["memberid"]

        # Insert into billing
        supabase.table("billing").insert({
            "memberid": member_id,
            "billtype": bill_type,
            "billdate": bill_date,
            "duedate": due_date,
            "status": status,
            "amountdue": amountdue
        }).execute()

        return redirect(url_for('views.admin_billing_payment'))

    return render_template("admin_create_bill.html")

@views.route('/admin/payment/record', methods=['GET'])
def admin_payment_record():
    return render_template('admin_record_payment.html')

# -- ADMIN COMMITTEE MANAGEMENT --
@views.route('/admin/committees')
def admin_committee_dashboard():
    return render_template('admin_committee_dashboard.html')

@views.route('/admin/committees/view')
def admin_committee_view():
    try:
        # Fetch all committees
        committees_result = supabase.table("committee").select("committeeid, name").execute()
        committees = committees_result.data

        enriched_committees = []

        for committee in committees:
            committee_id = committee["committeeid"]
            name = committee["name"]

            # Count the number of members for this committee
            members_result = supabase.table("committeemember") \
                                     .select("memberid") \
                                     .eq("committeeid", committee_id) \
                                     .execute()
            total_members = len(members_result.data)

            enriched_committees.append({
                "name": name,
                "total_members": total_members
            })

        return render_template("admin_committee_list.html", committees=enriched_committees)

    except Exception as e:
        print("Error fetching committee data:", e)
        return render_template("admin_committee_list.html", committees=[])
    
@views.route('/admin/committees/members', methods=['GET', 'POST'])
def admin_committee_manage():
    selected_event_id = request.args.get('event_id')
    selected_committee_id = request.args.get('committee_filter')

    events_data = supabase.table("event").select("eventid, name").execute().data
    all_committees = supabase.table("committee").select("committeeid, name, eventid").execute().data

    member_data = supabase.table("committeemember").select("""
        committeememberid,
        committeeid,
        position,
        status,
        committee (
            name
        ),
        member:memberid (
            individual (
                firstname,
                lastname
            )
        )
    """).eq("status", "Approved").execute().data

    return render_template(
        "admin_committee_manage_members.html",
        members=member_data,  # ✅ this one
        events=events_data,
        all_committees=all_committees,
        selected_event_id=selected_event_id,
        selected_committee_id=selected_committee_id or "all"
    )

@views.route('/admin/committee/add_member', methods=['POST'])
def add_committee_member():
    member_name = request.form.get("member_name")
    member_position = request.form.get("member_position")
    event_id = request.form.get("event_id")
    committee_id = request.form.get("member_committee")
    review_note = request.form.get("review_note")
    member_id = request.form.get("member_id")

    if not all([member_name, member_position, event_id, committee_id, member_id]):
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("views.admin_committee_manage"))

    supabase.table("committeemember").insert({
        "committeeid": committee_id,
        "memberid": member_id,
        "position": member_position,
        "applicationdate": date.today().isoformat(),
        "status": "Approved",
        "reviewnotes": review_note
    }).execute()

    flash("Committee member added successfully!", "success")
    return redirect(url_for("views.admin_committee_manage"))

@views.route('/admin/committee/members/delete/<int:memberid>', methods=['POST'])
def delete_committee_manage(memberid):
    try:
        supabase.table("committeemember").delete().eq("committeememberid", memberid).execute()
    except Exception as e:
        print("Error deleting member:", e)

    return redirect(url_for('views.admin_committee_manage'))

@views.route('/admin/committees/status')
def admin_committee_status():
    applications = supabase.table("committeemember").select("""
        committeememberid,
        position,
        status,
        committee (
            name
        ),
        member:memberid (
            individual (
                firstname,
                lastname
            )
        )
    """).eq("status", "Pending").execute().data

    return render_template("admin_committee_application_status.html", applications=applications)

@views.route('/admin/committees/application/<int:memberid>/approve', methods=['POST'])
def approve_committee_member(memberid):
    supabase.table("committeemember").update({"status": "Approved"}).eq("committeememberid", memberid).execute()
    return redirect(url_for('views.admin_committee_application_status'))

# Route to handle rejection
@views.route('/admin/committees/application/<int:memberid>/reject', methods=['POST'])
def reject_committee_member(memberid):
    supabase.table("committeemember").update({"status": "Rejected"}).eq("committeememberid", memberid).execute()
    return redirect(url_for('views.admin_committee_application_status'))

@views.route('/admin/committees/roles')
def admin_committee_roles():
    return render_template('admin_committee_role_assignment.html')

# -- STAFF MANAGEMENT --
@views.route('/admin/staff')
def admin_staff_management():
    return render_template('admin_staff_management.html')

@views.route('/admin/staff/manage', methods=['GET', 'POST'])
def admin_staff_manage():
    edit_id = request.args.get('edit_id', type=int)

    if request.method == 'POST':
        full_name = request.form.get('staff_name')
        email = request.form.get('staff_email')
        role = request.form.get('staff_role')

        # Split full name (optional: more validation can be added)
        names = full_name.strip().split()
        firstname = names[0]
        lastname = names[-1] if len(names) > 1 else ''
        middlename = ' '.join(names[1:-1]) if len(names) > 2 else ''

        try:
            # Save to Supabase
            supabase.table("staff").insert({
                "firstname": firstname,
                "middlename": middlename,
                "lastname": lastname,
                "email": email,
                "role": role,
                "username": email,  # Default username as email
                "password": "password123",  # Replace with secure logic
                "fullname": full_name
            }).execute()
        except Exception as e:
            print("Error inserting staff:", e)

        return redirect(url_for('views.admin_staff_manage'))

    # For GET request, fetch all staff accounts
    try:
        staff_data = supabase.table("staff").select("staffid, firstname, middlename, lastname, email, role").execute().data
    except Exception as e:
        print("Error fetching staff:", e)
        staff_data = []

    return render_template("admin_staff_manage_account.html", staff=staff_data)

@views.route('/admin/staff/update/<int:staffid>', methods=['POST'])
def update_staff(staffid):
    try:
        full_name = request.form.get('staff_name')
        email = request.form.get('staff_email')
        role = request.form.get('staff_role')

        # Split full name
        names = full_name.strip().split()
        firstname = names[0]
        lastname = names[-1] if len(names) > 1 else ''
        middlename = ' '.join(names[1:-1]) if len(names) > 2 else ''

        response = supabase.table("staff").update({
            "firstname": firstname,
            "middlename": middlename,
            "lastname": lastname,
            "email": email,
            "role": role,
            "fullname": full_name
        }).eq("staffid", staffid).execute()

        print("Update Response:", response)

    except Exception as e:
        print("Update Error:", e)

    return redirect(url_for('views.admin_staff_manage'))

@views.route('/admin/staff/delete/<int:staffid>', methods=['POST'])
def delete_staff(staffid):
    try:
        supabase.table("staff").delete().eq("staffid", staffid).execute()
    except Exception as e:
        print("Error deleting staff:", e)

    return redirect(url_for('views.admin_staff_manage'))

@views.route('/admin/staff/roles', methods=['GET', 'POST'])
def admin_staff_roles():
    if request.method == 'POST':
        staffid = request.form.get('staffid')
        new_role = request.form.get('new_role')

        try:
            update_result = supabase.table("staff").update({"role": new_role}).eq("staffid", staffid).execute()
            flash("Role updated successfully!", "success")
        except Exception as e:
            print("Error updating role:", e)
            flash("Error updating role.", "error")

        return redirect(url_for('views.admin_staff_roles'))

    try:
        staff_list = supabase.table("staff").select("staffid, firstname, middlename, lastname, email, role").execute().data
    except Exception as e:
        print("Error fetching staff list:", e)
        staff_list = []

    return render_template("admin_staff_assign_roles.html", staff=staff_list)

# -- MEMBER DASHBOARD --
@views.route('/user/dashboard', methods=['GET'])
def userdashboard():
    print("Session data:", session)
    if session.get('user_type') != 'individual':
        return redirect(url_for('auth.login'))
    
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
    if session.get('user_type') != 'individual':
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
    if session.get('user_type') != 'individual':
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
    
# -- INSTITUTIONAL DASHBOARD --
@views.route('/institutional/dashboard')
def institutional_dashboard():
    if session.get('user_type') != 'institution':
        return redirect(url_for('auth.login'))

    member_id = session.get('member_id')

    # 🔹 Get organizationid and schoolid of the logged-in institution
    inst_resp = supabase.table('institutional') \
        .select('organizationid, schoolid') \
        .eq('memberid', member_id) \
        .maybe_single() \
        .execute()

    if not inst_resp or not inst_resp.data:
        return "Institutional record not found", 404

    org_id = inst_resp.data.get('organizationid')
    school_id = inst_resp.data.get('schoolid')

    # 🔹 Get individual member IDs under this institution
    individual_ids = []
    individual_query = supabase.table('individual').select('memberid')

    if org_id:
        individual_query = individual_query.eq('organizationid', org_id)
    if school_id:
        individual_query = individual_query.eq('schoolid', school_id)

    individual_resp = individual_query.execute()
    if individual_resp.data:
        individual_ids = [row['memberid'] for row in individual_resp.data]

    # 1️⃣ Total Registered Members
    total_registered = len(individual_ids)

    # 2️⃣ Active Memberships (from institutionmembershipcapacity)
    capacity_resp = supabase.table('institutionmembershipcapacity') \
        .select('currentlyregistered') \
        .eq('institutionid', member_id) \
        .execute()

    active_memberships = sum(row['currentlyregistered'] for row in capacity_resp.data) if capacity_resp.data else 0

    # 3️⃣ Pending Membership Registrations of individuals
    pending_count = 0
    if individual_ids:
        pending_resp = supabase.table('membershipregistration') \
            .select('membershipregistrationid') \
            .in_('memberid', individual_ids) \
            .eq('status', 'Pending') \
            .execute()
        pending_count = len(pending_resp.data) if pending_resp.data else 0

    # 4️⃣ Upcoming Events (from today onward)
    today = datetime.today().strftime('%Y-%m-%d')
    event_resp = supabase.table('event') \
        .select('name, eventdate') \
        .gt('eventdate', today) \
        .order('eventdate') \
        .execute()
    upcoming_events = event_resp.data if event_resp and event_resp.data else []

    # 🔚 Render Template
    return render_template(
        'institutional_dashboard.html',
        total_registered=total_registered,
        active_memberships=active_memberships,
        pending_count=pending_count,
        upcoming_events=upcoming_events
    )

@views.route('/institutional/profile', methods=['GET', 'POST'])
def institutional_profile():
    if session.get('user_type') != 'institution':
        return redirect(url_for('auth.login'))

    member_id = session.get('member_id')

    if request.method == 'POST':
        data = request.get_json()
        # Password validation
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Get existing user
        user_resp = supabase.table('member').select('password').eq('memberid', member_id).maybe_single().execute()
        if not user_resp.data:
            return jsonify({'message': 'Member not found'}), 404

        hashed_pw = user_resp.data['password']

        if current_password and new_password:
            if not check_password_hash(hashed_pw, current_password):
                return jsonify({'message': 'Incorrect current password'}), 400

            new_hashed = generate_password_hash(new_password)
            supabase.table('member').update({'password': new_hashed}).eq('memberid', member_id).execute()

        # Update personal info
        update_data = {
            'streetaddress': data.get('streetaddress'),
            'emergencycontactname': data.get('emergencycontactname'),
            'emergencycontactnumber': data.get('emergencycontactnumber'),
            'region': data.get('region'),
            'province': data.get('province'),
            'city': data.get('city'),
            'barangay': data.get('barangay'),
            'phone': data.get('phone')
        }

        supabase.table('member').update(update_data).eq('memberid', member_id).execute()

        return jsonify({'message': 'Profile updated successfully'})

    # GET request - fetch profile data
    member_resp = supabase.table('member').select('*').eq('memberid', member_id).maybe_single().execute()
    inst_resp = supabase.table('institutional').select('*').eq('memberid', member_id).maybe_single().execute()

    if not member_resp.data or not inst_resp.data:
        return "Institutional profile not found", 404

    member = member_resp.data
    inst = inst_resp.data

    # Fetch location names
    region_name = get_location_name('region', 'regionid', member['region'])
    province_name = get_location_name('province', 'provinceid', member['province'])
    city_name = get_location_name('city', 'cityid', member['city'])
    barangay_name = get_location_name('barangay', 'barangayid', member['barangay'])

    return render_template(
        'institutional_profile.html',
        institution_name=inst.get('institutionalname', ''),
        institution_code=inst.get('schoolid') or inst.get('organizationid'),
        institution_type=inst.get('type'),
        fullname=f"{inst['representativefirstname']} {inst['representativemiddlename']} {inst['representativelastname']}",
        phone=inst['representativecontactnumber'],
        email=member['email'],
        streetaddress=member['streetaddress'],
        emergency_contact_name=member['emergencycontactname'],
        emergency_contact=member['emergencycontactnumber'],
        region_name=region_name,
        province_name=province_name,
        city_name=city_name,
        barangay_name=barangay_name,
        region_id=member['region'],
        province_id=member['province'],
        city_id=member['city'],
        barangay_id=member['barangay']
    )

def get_location_name(table, id_field, id_value):
    if not id_value:
        return ''
    res = supabase.table(table).select('*').eq(id_field, id_value).maybe_single().execute()
    if not res.data:
        return ''
    return res.data.get(f"{table}name", '')

@views.route('/institutional/member/management')
def institutional_member_management():
    if session.get('user_type') != 'institution':
        return redirect(url_for('views.login'))

    member_id = session.get('member_id')
    if not member_id:
        return "Unauthorized", 401

    # 🔸 Get institutional data (org/school IDs)
    inst_resp = supabase.table('institutional') \
        .select('institutionalname, organizationid, schoolid') \
        .eq('memberid', member_id) \
        .maybe_single() \
        .execute()

    if not inst_resp or not inst_resp.data:
        return "Institutional data not found", 404

    institutionalname = inst_resp.data.get('institutionalname')
    org_id = inst_resp.data.get('organizationid')
    school_id = inst_resp.data.get('schoolid')

    # 🔸 Fetch individuals under institution
    individual_query = supabase.table("individual").select("memberid, firstname, middlename, lastname")
    if org_id:
        individual_query = individual_query.eq("organizationid", org_id)
    if school_id:
        individual_query = individual_query.eq("schoolid", school_id)

    individual_result = individual_query.execute()
    individual_members = individual_result.data if individual_result.data else []

    member_ids = [m["memberid"] for m in individual_members]

    # 🔸 Get Active Memberships
    active_members = []
    if member_ids:
        registration_resp = supabase.table("membershipregistration") \
            .select("memberid") \
            .eq("status", "Active") \
            .in_("memberid", member_ids) \
            .execute()

        active_ids = [r["memberid"] for r in registration_resp.data]

        # Filter individuals who are active
        for person in individual_members:
            if person["memberid"] in active_ids:
                # Get member info (email, joindate)
                member_data = supabase.table("member") \
                    .select("email, joindate") \
                    .eq("memberid", person["memberid"]) \
                    .maybe_single() \
                    .execute().data

                active_members.append({
                    "fullname": f"{person['firstname']} {person.get('middlename', '')} {person['lastname']}".strip(),
                    "email": member_data["email"] if member_data else "N/A",
                    "joindate": member_data["joindate"] if member_data else "N/A"
                })

    # 🔸 Get Pending Memberships
    pending_members = []
    if member_ids:
        pending_resp = supabase.table("membershipregistration") \
            .select("memberid") \
            .eq("status", "Pending") \
            .in_("memberid", member_ids) \
            .execute()

        pending_ids = [p["memberid"] for p in pending_resp.data]

        for person in individual_members:
            if person["memberid"] in pending_ids:
                pending_members.append({
                    "membershipregistrationid": pending_resp.data[0]["memberid"],  # or fetch properly
                    "fullname": f"{person['firstname']} {person.get('middlename', '')} {person['lastname']}".strip()
                })

    return render_template(
        "institutional_member_management.html",
        pending_members=pending_members,
        active_members=active_members,
        institutionalname=institutionalname
    )

@views.route('/institutional/update_status', methods=['POST'])
def update_member_status():
    membership_id = request.form.get("membershipregistrationid")
    action = request.form.get("action")

    new_status = "Active" if action == "approve" else "Rejected"

    supabase.table("membershipregistration") \
        .update({"status": new_status}) \
        .eq("membershipregistrationid", membership_id) \
        .execute()

    return redirect(url_for('views.institutional_member_management'))

@views.route('/institutional/membership/details')
def institutional_membership_details():
    if session.get('user_type') != 'institution':
        return redirect(url_for('auth.login'))

    member_id = session.get('member_id')

    # 🔸 Get capacity + typeid
    capacity_resp = supabase.table("institutionmembershipcapacity") \
        .select("maximumcapacity, currentlyregistered, membershiptypeid, membershiptype(name, benefits)") \
        .eq("institutionid", member_id) \
        .maybe_single() \
        .execute()

    capacity_data = capacity_resp.data if capacity_resp.data else {}

    # 🔸 Get membership registration history
    reg_history_resp = supabase.table("membershipregistration") \
        .select("startdate, enddate, status, typeid, membershiptype(name)") \
        .eq("memberid", member_id) \
        .order("startdate", desc=True) \
        .execute()

    return render_template(
        'institutional_membership_details.html',
        capacity=capacity_data,
        reg_history=reg_history_resp.data or []
    )

@views.route('/institutional/billing')
def institutional_billing_payment():
    if session.get('user_type') != 'institution':
        return redirect(url_for('auth.login'))

    member_id = session.get('member_id')

    # Get billing records of the institutional member
    billing_resp = supabase.table('billing').select('*').eq('memberid', member_id).order('billdate', desc=True).execute()
    billings = billing_resp.data if billing_resp and billing_resp.data else []

    return render_template('institutional_billing_payment.html', billings=billings)

UPLOAD_FOLDER = 'static/uploads'  # Make sure this exists
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/institutional/payment', methods=['GET', 'POST'])
def institutional_payment():
    if session.get('user_type') != 'institution':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        membership_type = request.form.get('membership-type')
        file = request.files.get('proof')
        member_id = session.get('member_id')

        if not membership_type or not file or not allowed_file(file.filename):
            flash('All fields are required and file must be an image or PDF.')
            return redirect(request.url)

        # Save file to local folder
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{member_id}_{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        # Store in Supabase
        supabase.table("payment").insert({
            "memberid": member_id,
            "amount": 1000 if membership_type == "basic" else 2000,
            "status": "Pending",
            "proof": file_path,
            "paymentdate": datetime.now().strftime('%Y-%m-%d')
        }).execute()

        flash('Payment submitted successfully.')
        return redirect(url_for('views.institutional_billing_payment'))

    return render_template("institutional_payment.html")


# -- TO BE DELETED -- 
# @views.route('/admin/committees/members/update/<int:memberid>', methods=['POST'])
# def update_committee_manage(memberid):
#     name = request.form.get('name', '').strip()
#     email = request.form.get('member_email')
#     role = request.form.get('member_role')

#     names = name.strip().split()
#     firstname = names[0]
#     lastname = names[-1] if len(names) > 1 else ''
#     middlename = ' '.join(names[1:-1]) if len(names) > 2 else ''

#     try:
#         supabase.table("committeemember").update({
#             "firstname": firstname,
#             "middlename": middlename,
#             "lastname": lastname,
#             "email": email,
#             "role": role,
#             "fullname": name
#         }).eq("committeememberid", memberid).execute()
#     except Exception as e:
#         print("Error updating member:", e)

#     return redirect(url_for('views.admin_committee_manage'))