from flask import Blueprint, jsonify, render_template, abort, request
from . import models
from .supabase_client import supabase
from datetime import datetime

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