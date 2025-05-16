from flask import Blueprint
from src.api.controllers.resume_controller import ResumeController
from src.api.middlewares.authMiddleware import AuthMiddleware as authMiddleware

resumeRoute = Blueprint('resumeRoute', __name__)

@resumeRoute.route('/resume/upload', methods=['POST'])
@authMiddleware.ValidateToken
def uploadResume(data):
    resumeCtrl = ResumeController()
    return resumeCtrl.uploadResume(data)