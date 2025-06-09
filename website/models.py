from datetime import datetime
from .supabase_client import supabase


# --- Member ---
def get_all_members(supabase):
    try:
        response = supabase.table('member').select('*').execute()
        if response.data is None:
            return None, "No data found"
        return response.data, None
    except Exception as e:
        return None, str(e)

