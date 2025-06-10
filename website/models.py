from datetime import datetime
from .supabase_client import supabase

def iso_date(value):
     try:
          return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
     except Exception:
          return None

# --- MEMBER ---
def get_all_members(supabase):
    try:
        response = supabase.table('member').select('*').execute()
        if response.data is None:
            return None, "No data found"
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_member_by_id(supabase, memberid):
    try:
        response = supabase.table("member").select("*").eq("memberid", memberid).single().execute()
        if response.data is None:
                return None, "Member not found"
        return response.data, None
    except Exception as e:
         return None, f"Failed to fetch member: {str(e)}"

def create_member(supabase, member_data):
    if "dateofbirth" in member_data:
        iso = iso_date(member_data["dateofbirth"])
        if iso is None:
            return None, "Invalid DateOfBirth format, expected YYYY-MM-DD"
        member_data["dateofbirth"] = iso
    
    if "joindate" not in member_data:
        member_data["joindate"] = datetime.utcnow().isoformat()
    try:
        response = supabase.table("member").insert(member_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create member: {str(e)}"

def update_member(supabase, memberid, update_data):
    if "dateofbirth" in update_data:
        iso = iso_date(update_data["dateofbirth"])
        if iso is None:
            return None, "Invalid DateOfBirth format, expected YYYY-MM-DD"
        update_data["dateofbirth"] = iso
    try:
        response = supabase.table("member").update(update_data).eq("memberid", memberid).select("*").single().execute()
        if response.data is None:
            return None, "Member not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update member: {str(e)}"
    
def delete_member(supabase, memberid):
    try:
        response = supabase.table("member").delete().eq("memberid", memberid).execute()
        if response.count == 0:
            return False, "Member not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete member: {str(e)}"
    
# --- MEMBERSHIP TYPES ---

def get_all_membership_types(supabase):
    try:
        response = supabase.table("membershiptype").select("*").order("typeid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch membership types: {str(e)}"
    
def get_membership_type_by_id(supabase, typeid):
    try:
        response = supabase.table("membershiptype").select("*").eq("typeid", typeid).single().execute()
        if response.data is None:
            return None, "Membership type not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch membership type: {str(e)}"

def create_membership_type(supabase, type_data):
    try:
        response = supabase.table("membershiptype").insert(type_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create membership type: {str(e)}"

def update_membership_type(supabase, typeid, update_data):
    try:
        response = supabase.table("membershiptype").update(update_data).eq("typeid", typeid).select("*").single().execute()
        if response.data is None:
            return None, "Membership type not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update membership type: {str(e)}"
    
def delete_membership_type(supabase, typeid):
    try:
        response = supabase.table("membershiptype").delete().eq("typeid", typeid).execute()
        if response.count == 0:
            return False, "Membership type not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete membership type: {str(e)}"
    
# --- MEMBERSHIP REGISTRATION ---
def get_all_membership_registrations(supabase):
    try:
        response = supabase.table("membershipregistration").select("*").order("membershipregistrationid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch membership registrations: {str(e)}"

def get_membership_registration_by_id(supabase, regid):
    try:
        response = supabase.table("membershipregistration").select("*").eq("memberid", regid).single().execute()
        if response.data is None:
            return None, "Membership registration not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch membership registration: {str(e)}"

def create_membership_registration(supabase, reg_data):
    try:
        response = supabase.table("membershipregistration").insert(reg_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create membership registration: {str(e)}"
    
def update_membership_registration(supabase, regid, update_data):
    try:
        response = supabase.table("membershipregistration").update(update_data).eq("memberid", regid).select("*").single().execute()
        if response.data is None:
            return None, "Membership registration not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update membership registration: {str(e)}"
    
def delete_membership_registration(supabase, regid):
    try:
        response = supabase.table("membershipregistration").delete().eq("memberid", regid).execute()
        if response.count == 0:
            return False, "Membership registration not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete membership registration: {str(e)}"
    
# --- PAYER ---
def get_all_payers(supabase):
    try:
        response = supabase.table("payer").select("*").order("payerid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch payers: {str(e)}"
    
def get_payer_by_id(supabase, payerid):
    try:
        response = supabase.table("payer").select("*").eq("payerid", payerid).single().execute()
        if response.data is None:
            return None, "Payer not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch payer: {str(e)}"
    
def create_payer(supabase, payer_data):
    try:
        response = supabase.table("payer").insert(payer_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create payer: {str(e)}"
    
def update_payer(supabase, payerid, update_data):
    try:
        response = supabase.table("payer").update(update_data).eq("payerid", payerid).select("*").single().execute()
        if response.data is None:
            return None, "Payer not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update payer: {str(e)}"
    
def delete_payer(supabase, payerid):
    try:
        response = supabase.table("payer").delete().eq("payerid", payerid).execute()
        if response.count == 0:
            return False, "Payer not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete payer: {str(e)}"
    
# --- BILLING ---
def get_all_billing(supabase):
    try:
        response = supabase.table("billing").select("*").order("billingid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch billing: {str(e)}"
    
def get_billing_by_id(supabase, billingid):
    try:
        response = supabase.table("billing").select("*").eq("billingid", billingid).single().execute()
        if response.data is None:
            return None, "Billing not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch billing: {str(e)}"
    
def create_billing(supabase, billing_data):
    try:
        response = supabase.table("billing").insert(billing_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create billing: {str(e)}"
    
def update_billing(supabase, billingid, update_data):
    try:
        response = supabase.table("billing").update(update_data).eq("billingid", billingid).select("*").single().execute()
        if response.data is None:
            return None, "Billing not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update billing: {str(e)}"
    
def delete_billing(supabase, billingid):
    try:
        response = supabase.table("billing").delete().eq("billingid", billingid).execute()
        if response.count == 0:
            return False, "Billing not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete billing: {str(e)}"
    
# --- PAYMENTS ---
def get_all_payments(supabase):
    try:
        response = supabase.table("payment").select("*").order("paymentid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch payments: {str(e)}"
    
def get_payment_by_id(supabase, paymentid):
    try:
        response = supabase.table("payment").select("*").eq("paymentid", paymentid).single().execute()
        if response.data is None:
            return None, "Payment not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch payment: {str(e)}"
def create_payment(supabase, payment_data):
    try:
        response = supabase.table("payment").insert(payment_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create payment: {str(e)}"
    
def update_payment(supabase, paymentid, update_data):
    try:
        response = supabase.table("payment").update(update_data).eq("paymentid", paymentid).select("*").single().execute()
        if response.data is None:
            return None, "Payment not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update payment: {str(e)}"
def delete_payment(supabase, paymentid):
    try:
        response = supabase.table("payment").delete().eq("paymentid", paymentid).execute()
        if response.count == 0:
            return False, "Payment not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete payment: {str(e)}"
    
# --- COMMITTEES ---
def get_all_committees(supabase):
    try:
        response = supabase.table("committee").select("*").order("committeeid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch committees: {str(e)}"
    
def get_committee_by_id(supabase, committeeid):
    try:
        response = supabase.table("committee").select("*").eq("committeeid", committeeid).single().execute()
        if response.data is None:
            return None, "Committee not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch committee: {str(e)}"
    
def create_committee(supabase, committee_data):
    try:
        response = supabase.table("committee").insert(committee_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create committee: {str(e)}"
def update_committee(supabase, committeeid, update_data):
    try:
        response = supabase.table("committee").update(update_data).eq("committeeid", committeeid).select("*").single().execute()
        if response.data is None:
            return None, "Committee not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update committee: {str(e)}"
def delete_committee(supabase, committeeid):
    try:
        response = supabase.table("committee").delete().eq("committeeid", committeeid).execute()
        if response.count == 0:
            return False, "Committee not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete committee: {str(e)}"
    
# --- COMMITTEE MEMBERS ---
def get_all_committee_members(supabase):
    try:
        response = supabase.table("committeemember").select("*").limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch committee members: {str(e)}"
    
def get_committee_member(supabase, committeeid, memberid):
    try:
        response = supabase.table("committeemember").select("*").eq("committeeid", committeeid).eq("memberid", memberid).single().execute()
        if response.data is None:
            return None, "Committee member not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch committee member: {str(e)}"
    
def create_committee_member(supabase, committee_member_data):
    try:
        response = supabase.table("committeemember").insert(committee_member_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create committee member: {str(e)}"
    
def update_committee_member(supabase, committeeid, memberid, update_data):
    try:
        response = supabase.table("committeemember").update(update_data).eq("committeeid", committeeid).eq("memberid", memberid).select("*").single().execute()
        if response.data is None:
            return None, "Committee member not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update committee member: {str(e)}"
    
def delete_committee_member(supabase, committeeid, memberid):
    try:
        response = supabase.table("committeemember").delete().eq("committeeid", committeeid).eq("memberid", memberid).execute()
        if response.count == 0:
            return False, "Committee member not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete committee member: {str(e)}"
    
# --- EVENTS ---
def get_all_events(supabase):
    try:
        response = supabase.table("event").select("*").order("eventid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch events: {str(e)}"
    
def get_event_by_id(supabase, eventid):
    try:
        response = supabase.table("event").select("*").eq("eventid", eventid).single().execute()
        if response.data is None:
            return None, "Event not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch event: {str(e)}"
    
def create_event(supabase, event_data):
    try:
        response = supabase.table("event").insert(event_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create event: {str(e)}"
    
def update_event(supabase, eventid, update_data):
    try:
        response = supabase.table("event").update(update_data).eq("eventid", eventid).select("*").single().execute()
        if response.data is None:
            return None, "Event not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update event: {str(e)}"
    
def delete_event(supabase, eventid):
    try:
        response = supabase.table("event").delete().eq("eventid", eventid).execute()
        if response.count == 0:
            return False, "Event not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete event: {str(e)}"
    
# --- EVENT REGISTRATION ---
def get_all_event_registrations(supabase):
    try:
        response = supabase.table("eventregistration").select("*").order("registrationid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch event registrations: {str(e)}"
    
def get_event_registration_by_id(supabase, registrationid):
    try:
        response = supabase.table("eventregistration").select("*").eq("registrationid", registrationid).single().execute()
        if response.data is None:
            return None, "Event registration not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch event registration: {str(e)}"
    
def create_event_registration(supabase, registration_data):
    try:
        response = supabase.table("eventregistration").insert(registration_data).select("*").execute()
        return response.data[0], None
    except Exception as e:
        return None, f"Failed to create event registration: {str(e)}"
    
def update_event_registration(supabase, registrationid, update_data):
    try:
        response = supabase.table("eventregistration").update(update_data).eq("registrationid", registrationid).select("*").single().execute()
        if response.data is None:
            return None, "Event registration not found for update"
        return response.data, None
    except Exception as e:
        return None, f"Failed to update event registration: {str(e)}"
    
def delete_event_registration(supabase, registrationid):
    try:
        response = supabase.table("eventregistration").delete().eq("registrationid", registrationid).execute()
        if response.count == 0:
            return False, "Event registration not found to delete"
        return True, None
    except Exception as e:
        return False, f"Failed to delete event registration: {str(e)}"
    
# --- STAFF ---
def get_all_staff(supabase):
    try:
        response = supabase.table("staff").select("staffid,firstname,middlename,lastname,username,fullname,role,email").order("staffid", desc=False).limit(100).execute()
        if response.data is None:
            return [], None
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch staff: {str(e)}"
    
def get_staff_by_id(supabase, staffid):
    try:
        response = supabase.table("staff").select("staffid,firstname,middlename,lastname,username,fullname,role,email").eq("staffid", staffid).single().execute()
        if response.data is None:
            return None, "Staff not found"
        return response.data, None
    except Exception as e:
        return None, f"Failed to fetch staff: {str(e)}"