from flask import Blueprint, Response, abort, request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, json_required

api = Api(Blueprint('restaurant-api', __name__))


@api.resource('/restaurant')
class RestaurantList(BaseResource):
    def get(self):
        """
        식당 목록 조회

        TODO 필터 방식에 대해 협의하고 추가적으로 작업이 필요함
        """


@api.resource('/restaurant/<restaurant_id>')
class Restaurant(BaseResource):
    def get(self, restaurant_id):
        """
        식당 정보 조회
        """


@api.resource('/menu/<restaurant_id>')
class MenuList(BaseResource):
    def get(self, restaurant_id):
        """
        특정 식당의 메뉴 목록 조회
        """


@api.resource('/menu/<menu_id>')
class Menu(BaseResource):
    def get(self, menu_id):
        """
        특정 메뉴의 정보 조회
        """


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
