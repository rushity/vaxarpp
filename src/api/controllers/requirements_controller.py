from flask.views import MethodView
from flask import request, jsonify
import json
from src.constants import infoConstant as constant
from src.utils.loggerUtils import CustomJSONFormatter as logger

class RequirementsController(MethodView):

    def handle(self):
        try:
            if request.method == "GET":
                with open("requirements.json") as f:
                    return jsonify(json.load(f))
            else:
                data = request.get_json()
                with open("requirements.json", "w") as f:
                    json.dump(data, f, indent=2)
                return jsonify({"message": "Requirements updated"})
        except Exception as e:
            logger.CreateLog("ERROR", "REQUIREMENTS_ERROR", 500, 310, str(e))
            return jsonify({"error": "Server error"}), 500