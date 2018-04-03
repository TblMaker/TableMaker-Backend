from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint('cart-api', __name__))


@api.resource('/cart')
class Cart(BaseResource):
    def get(self):
        """
        장바구니 목록 조회
        """

    def post(self):
        """
        장바구니에 메뉴 등록
        """