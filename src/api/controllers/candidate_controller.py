from flask.views import MethodView
from flask import request, jsonify
import json
from src.constants import infoConstant as constant
from src.utils.loggerUtils import CustomJSONFormatter as logger
from flask import send_from_directory, current_app

class CandidateController(MethodView):

    def getAll(self, data):
        try:
            with open("candidates.json", "r") as f:
                return jsonify(json.load(f))
        except Exception as e:
            logger.CreateLog("ERROR", "CANDIDATE_LIST_FAILED", 500, 210, str(e))
            return jsonify({"error": "Server error"}), 500

    def delete(self, data):
        try:
            email = request.get_json().get("email")
            with open("candidates.json", "r+") as f:
                candidates = json.load(f)
                updated = [c for c in candidates if c.get("email") != email]
                f.seek(0)
                f.truncate()
                json.dump(updated, f, indent=2)
            return jsonify({"message": "Candidate deleted"})
        except Exception as e:
            logger.CreateLog("ERROR", "CANDIDATE_DELETE_FAILED", 500, 220, str(e))
            return jsonify({"error": "Server error"}), 500

     def download_resume(self, filename):
        try:
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            return send_from_directory(upload_folder, filename, as_attachment=True)
        except Exception as e:
            logger.CreateLog("ERROR", "RESUME_DOWNLOAD_FAILED", 500, 230, str(e))
            return jsonify({"error": "File not found"}), 404   
