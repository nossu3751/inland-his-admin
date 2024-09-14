import os
import traceback
from flask import Blueprint, jsonify, request, abort
from app.api.v1.services.new_comer import NewComerService
from app.api.v1.utils.new_comer import *
from datetime import datetime, timedelta
import httplib2
from apiclient import discovery
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

new_comers_blueprint = Blueprint('new-comers', __name__, url_prefix="/api/v1/new-comers")

@new_comers_blueprint.route('/<int:new_comer_id>', methods=['GET'])
def get_new_comer(new_comer_id):
    new_comer = NewComerService.get_new_comer_by_id(new_comer_id)

    if not new_comer:
        abort(404, description=f"New Comer with ID {new_comer_id} not found")

    return jsonify(format_new_comer(new_comer)), 200

@new_comers_blueprint.route('/<int:new_comer_id>', methods=['DELETE'])
def delete_new_comer(new_comer_id):
    try:
        NewComerService.delete_new_comer_by_id(new_comer_id)
        return jsonify("new commer successfully deleted"), 200
    except Exception:
        return jsonify("ServerError"), 500

@new_comers_blueprint.route('/<int:new_comer_id>', methods=['PUT'])
def update_new_comer(new_comer_id):
    data = request.get_json()

    if not data:
        abort(400, description="Missing or invalid request data")

    updated_new_comer = NewComerService.update_new_comer(new_comer_id, data)

    if not updated_new_comer:
        abort(404, description=f"New Comer with ID {new_comer_id} not found")

    return jsonify(format_new_comer(updated_new_comer)), 200

@new_comers_blueprint.route('/', methods=['GET'])
def get_new_comers():
    try:
        new_comers = NewComerService.get_all_new_comers()
        if new_comers:
            return jsonify(format_new_comers(new_comers))
        else:
            return jsonify({"data": [], "error":"No New Comers Found"}), 200
    except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "Error occurred: {}".format(str(e))}), 500
    
@new_comers_blueprint.route('/googleSheet', methods=["POST"])
def send_new_comer_to_spreadsheet():
    try:
        data = request.get_json()
        if "new_comer_id" in data:
            new_comer_id = data["new_comer_id"]
        else:
            return jsonify({"error":"No new comers to post"}), 409
        if "spreadsheet_link" in data:
            spreadsheet_link = str(data["spreadsheet_link"])
            try:
                spreadsheet_id = spreadsheet_link.split("docs.google.com/spreadsheets/d/")[1]
                if "/" in spreadsheet_id:
                    spreadsheet_id = spreadsheet_id.split("/")[0]

            except Exception as e:
                return jsonify({"error":"spreadsheet link format is wrong"}), 409
        else:
            return jsonify({"error":"Missing spreadsheet link"})
        if "sheet" in data:
            sheet = data["sheet"]
        else:
            sheet = "Sheet1"
        
        if new_comer_id == "all":
            post_data = format_new_comers_for_google_sheet(NewComerService.get_all_new_comers())
        elif isinstance(new_comer_id, int):
            post_data = [format_new_comer_for_google_sheet(NewComerService.get_new_comer_by_id(new_comer_id))]

        scopes = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/drive.file"]

        secret_file = os.getenv("GOOGLE_SPREADSHEETS_SECRET")
        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
        credentials.refresh(Request())
        # access_token = credentials.token

        service = discovery.build('sheets', 'v4', credentials=credentials)
        try:
            _ = service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet}!A:A",
                valueInputOption='RAW',  # 'RAW' or 'USER_ENTERED' depending on how you want the data to be interpreted
                insertDataOption='INSERT_ROWS',  # This tells the API to insert new rows instead of overwriting
                body={
                    "values": post_data
                }
            ).execute()

            if new_comer_id == "all":
                all_new_comers = NewComerService.get_all_new_comers()
                for new_comer in all_new_comers:
                    NewComerService.delete_new_comer_by_id(new_comer.id)
            elif isinstance(new_comer_id, int):
                NewComerService.delete_new_comer_by_id(new_comer_id)
                
        except Exception:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "Error occurred: {}".format(str(e))}), 500


        return jsonify({"message": "Data successfully added to Google Sheets"}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Error occurred: {}".format(str(e))}), 500