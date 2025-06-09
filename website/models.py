from datetime import datetime
from .supabase_client import supabase

def iso_date(value):
     try:
          return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
     except Exception:
          return None

# --- Member ---
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