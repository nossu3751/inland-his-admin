import traceback
from flask import Blueprint, jsonify, request, abort
from app.api.v1.services.bulletin import BulletinService
from app.api.v1.utils.bulletin import *
from datetime import datetime, timedelta

bulletins_blueprint = Blueprint('bulletins', __name__, url_prefix="/api/v1/bulletins")

@bulletins_blueprint.route('/', methods=['POST'])
def upload_bulletin():
    try:
        data = request.json
        
        if not data:
            abort(400, description="Missing or invalid request data")

        date_posted = datetime.utcnow()
        sunday_date = (date_posted + timedelta(days=(6 - date_posted.weekday()))).date()
        
        if "sunday_date" not in data or data["sunday_date"] == None:
            data["sunday_date"] = sunday_date

        existing_bulletin = Bulletin.query.filter_by(sunday_date=data["sunday_date"]).first()
    
        if existing_bulletin:
            traceback.print_exc()
            return jsonify({
                "error": "BulletinExists",
            }), 409
        
        new_bulletin = BulletinService.create_bulletin(data)

        return jsonify(format_bulletin_data(new_bulletin)), 201
    except Exception:
        traceback.print_exc()
        return jsonify({
                "error": "ServerError",
        }), 500
        

@bulletins_blueprint.route('/<int:bulletin_id>', methods=['GET'])
def get_bulletin(bulletin_id):
    bulletin = BulletinService.get_bulletin_by_id(bulletin_id)

    if not bulletin:
        abort(404, description=f"Bulletin with ID {bulletin_id} not found")

    return jsonify(format_bulletin_data(bulletin)), 200

@bulletins_blueprint.route('/<int:bulletin_id>', methods=['DELETE'])
def delete_bulletin(bulletin_id):
    try:
        BulletinService.delete_bulletin_by_id(bulletin_id)
        return jsonify(""), 200
    except Exception:
        return jsonify("ServerError"), 500

@bulletins_blueprint.route('/<int:bulletin_id>', methods=['PUT'])
def update_bulletin(bulletin_id):
    data = request.get_json()

    if not data:
        abort(400, description="Missing or invalid request data")

    updated_bulletin = BulletinService.update_bulletin(bulletin_id, data)

    if not updated_bulletin:
        abort(404, description=f"Bulletin with ID {bulletin_id} not found")

    return jsonify(format_bulletin_data(updated_bulletin)), 200

@bulletins_blueprint.route('/', methods=['GET'])
def get_bulletins():
    try:
        bulletins = BulletinService.get_all_bulletins()
        if bulletins:
            return jsonify(format_bulletins_data(bulletins))
        else:
            return jsonify({"data": [], "error":"No Bulletins Found"}), 200
    except Exception as e:
                import traceback
                traceback.print_exc()
                return jsonify({"error": "Error occurred: {}".format(str(e))}), 500