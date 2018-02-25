from flask import Blueprint, Response, abort, request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, json_required

api = Api(Blueprint('auth-api', __name__))


@api.resource('/auth/sns')
class SNSAuth(BaseResource):
    @json_required('')
    def post(self):
        """
        SNS 계정 로그인
        """


@api.resource('/auth')
class Auth(BaseResource):
    @json_required('')
    def post(self):
        """
        서비스 자체 계정 로그인
        """
