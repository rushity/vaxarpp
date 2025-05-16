from flask import Blueprint
from src.api.controllers.requirements_controller import RequirementsController
from src.api.middlewares.authMiddleware import AuthMiddleware as authMiddleware

requirementsRoute = Blueprint('requirementsRoute', __name__)

@requirementsRoute.route('/requirements', methods=['GET', 'POST'])
@authMiddleware.ValidateToken
def Manage(data):
    ctrl = RequirementsController()
    return ctrl.handle()