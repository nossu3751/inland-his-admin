import traceback
from flask import Blueprint, jsonify, request, abort
from app.api.v1.services.app_patch import AppPatchService
from app.api.v1.utils.app_patch import *
from datetime import datetime, timedelta

app_patch_blueprint = Blueprint('app_patches', __name__, url_prefix="/api/v1/app_patches")

@app_patch_blueprint.route('/', methods=['POST'])
def post_app_patch():
    try:
        data = request.json
        
        if not data:
            abort(400, description="Missing or invalid request data")
        
        new_app_patch = AppPatchService.create_app_patch(data)

        return jsonify(format_app_patch(new_app_patch)), 201
    except Exception:
        traceback.print_exc()
        return jsonify({
                "error": "ServerError",
        }), 500
        
@app_patch_blueprint.route('/', methods=['GET'])
def get_app_patches():
    try:
        app_patches = AppPatchService.get_all_app_patches()
        if app_patches:
            return jsonify(format_app_patches(app_patches))
        else:
            return jsonify([]), 200
    except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "Error occurred: {}".format(str(e))}), 500