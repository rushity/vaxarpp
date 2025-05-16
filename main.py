from flask import Flask
from flask_cors import CORS
import yaml
import os

from src.api.routes.resume_routes import resumeRoute
from src.api.routes.auth_routes import authRoute
from src.api.routes.candidate_routes import candidateRoute
from src.api.routes.requirements_routes import requirementsRoute

with open("config.yaml") as f:
    config = yaml.safe_load(f)

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = config["app"]["upload_folder"]
app.secret_key = config["app"]["secret_key"]

app.register_blueprint(resumeRoute)
app.register_blueprint(authRoute)
app.register_blueprint(candidateRoute)
app.register_blueprint(requirementsRoute)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
