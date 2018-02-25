from flask import Blueprint, Response, abort, request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, json_required

api = Api(Blueprint('signup-api', __name__))


@api.resource('/signup/sns')
class SNSSignup(BaseResource):
    @json_required()
    def post(self):
        """
        SNS 계정 회원가입

        가입되지 않은 SNS ID일 경우 보통 auth 과정에서 자동으로 가입시켜 주지만,
        추가적인 정보들이 필요하므로 '실패' 상태를 두고 별도로 회원가입을 진행합니다.
        """


@api.resource('/check/email')
class CheckEmail(BaseResource):
    @json_required()
    def post(self):
        """
        이메일 존재 여부 검사
        """


@api.resource('/check/phone')
class CheckPhone(BaseResource):
    @json_required()
    def post(self):
        """
        핸드폰 번호 존재 여부 검사

        서비스 자체 계정과 SNS 계정 회원가입 시 모두 사용됩니다.
        """


@api.resource('/signup')
class Signup(BaseResource):
    @json_required()
    def post(self):
        """
        서비스 자체 게정 회원가입
        """


@api.resource('/certify/<url>')
class Certify(BaseResource):
    @json_required()
    def get(self, url):
        """
        서비스 자체 계정 이메일 인증
        """
