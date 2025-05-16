from flask import Blueprint
from src.api.controllers.candidate_controller import CandidateController
from src.api.middlewares.authMiddleware import AuthMiddleware as authMiddleware

candidateRoute = Blueprint('candidateRoute', __name__)

@candidateRoute.route('/candidate/list', methods=['GET'])
@authMiddleware.ValidateToken
def GetAll(data):
    ctrl = CandidateController()
    return ctrl.getAll(data)

@candidateRoute.route('/candidate/delete', methods=['POST'])
@authMiddleware.ValidateToken
def Delete(data):
    ctrl = CandidateController()
    return ctrl.delete(data)