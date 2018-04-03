from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint('menu-api', __name__))


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