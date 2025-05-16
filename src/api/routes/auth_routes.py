from flask import Blueprint
from src.api.controllers.auth_controller import AuthController
from src.api.middlewares.authMiddleware import AuthMiddleware as authMiddleware

authRoute = Blueprint('authRoute', __name__)

@authRoute.route('/auth/login', methods=['POST'])
def Login():
    ctrl = AuthController()
    return ctrl.signIn()