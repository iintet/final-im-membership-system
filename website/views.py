from flask import Blueprint, jsonify, current_app
views = Blueprint('views', __name__)

@views.route('/')
def homepage():
    return "Try"

@views.route('/members')
def get_members():
    #supabase = current_app.extensions['supabase']
    #response = supabase.client.from_('members').select('*').execute()
    #return jsonify(response.data)
    return "Members"
