from datetime import datetime, timedelta

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Api
from flasgger import swag_from

from app.docs.restaurant.restaurant import *
from app.models.restaurant import RestaurantModel
from app.views import BaseResource, json_required

from app.models.support.mongo_helper import mongo_to_dict
from utils.gps_operation_helper import get_distance_between_two_points

api = Api(Blueprint('restaurant-api', __name__))


@api.resource('/restaurant/<sector>')
class RestaurantList(BaseResource):
    def __init__(self):
        # self.PRICE_LEVEL = 1, 2, 3
        self.SORT_TYPE = 1, 2, 3, 4, 5

        super(RestaurantList, self).__init__()

    def _get_time_gap(self, reservation_time_str):
        """
        현재 시간과 예약 시간 사이의 gap을 분 단위로 리턴합니다.

        Attributes:
            reservation_time_str (str): 예약 시간(%H:%M)

        Returns:
            int: 현재 시간과 예약 시간 사이의 gap을 분 단위로 리턴합니다.
            예약 시간이 현재 시간보다 이를 경우 음수가 리턴됩니다.
        """
        now_time_str = str(datetime.now().time())[:5]
        now_time = datetime.strptime(now_time_str, '%H:%M')
        reservation_time = datetime.strptime(reservation_time_str, '%H:%M')

        time_gap_sec = int((reservation_time - now_time).total_seconds())

        return time_gap_sec // 60

    def _get_restaurant_objects(self, sector, reservation_count, reservation_time_str, time_gap_min):
        """
        요청 데이터에 맞춰 쿼리된 식당 리스트를 불러옵니다.

        Attributes:
            sector (str): 식당 종류
            '아무거나'일 경우 'all'

            reservation_count (int): 예약 인원 수

            reservation_time_str (str): 예약 시간(%H:%M)

            time_gap_min (int): 예약 시간까지의 분 단위 gap

        Returns:
            list: 예약 인원 수, 예약 시간, 예약 시간까지의 gap 조건에 맞는 식당 리스트
        """
        return RestaurantModel.objects(
            # price_level=price_level,
            min_reservation_count__gte=reservation_count,
            max_reservation_count__lte=reservation_count,
            open_time__gte=reservation_time_str,
            close_time__lte=reservation_time_str,
            reservation_gap_minutes__gte=time_gap_min
        ) if sector == 'all' else RestaurantModel.objects(
            sector=sector,
            # price_level=price_level,
            min_reservation_count__gte=reservation_count,
            max_reservation_count__lte=reservation_count,
            open_time__gte=reservation_time_str,
            close_time__lte=reservation_time_str,
            reservation_gap_minutes__gte=time_gap_min
        )

    def _get_sorted_restaurant_list(self, restaurants, sort_type, latitude, longitude):
        """
        요청의 sortType에 의해 정렬된 식당 리스트를 불러옵니다.

        Attributes:
            restaurants (list): RestaurantModel 객체로 이루어진 리스트

            sort_type (int): 정렬 타입

            latitude (float): 클라이언트의 위도

            longitude (float): 클라이언트의 경도

        Returns:
            list: 바로 response payload로 사용할 수 있도록 가공된 식당 리스트
        """
        restaurants_list = [mongo_to_dict(restaurant) for restaurant in restaurants]

        if sort_type == 1:
            # 예약 인기 높은 순
            today = datetime.today()
            seven_days_ago = today - timedelta(days=7)

            dates = [seven_days_ago + timedelta(days=i) for i in range((today - seven_days_ago).days + 1)]
            # 날짜 순회 용도

            for restaurant in restaurants_list:
                restaurant['reservation_count_sum'] = 0
                for date in dates:
                    date_str = str(date)[:10]

                    restaurant['reservation_count_sum'] += restaurant['reservation_count'].get(date_str, 0)

            restaurants_list.sort(key=lambda obj: obj['reservation_count_sum'], reverse=True)
        elif sort_type == 2:
            # 가까운 거리 ~ 먼 거리
            restaurants_list.sort(
                key=lambda obj: get_distance_between_two_points(
                    latitude,
                    longitude,
                    obj.latitude,
                    obj.longitude
                )
            )
        elif sort_type == 3:
            # 낮은 가격 ~ 높은 가격
            restaurants_list.sort(key=lambda obj: obj['price_avg'])
        elif sort_type == 4:
            # 높은 가격 ~ 낮은 가격
            restaurants_list.sort(key=lambda obj: obj['price_avg'], reverse=True)
        else:
            # 평점 높은 순
            restaurants_list.sort(key=lambda obj: obj['rating'], reverse=True)

        return [{
            'title': restaurant['name'],
            'rating': restaurant['rating'],
            'distance': get_distance_between_two_points(
                latitude,
                longitude,
                restaurant['latitude'],
                restaurant['longitude']
            )
        } for restaurant in restaurants_list]

    @swag_from(RESTAURANT_LIST_GET)
    def get(self, sector):
        """
        식당 목록 조회
        """
        reservation_count = int(request.args.get('reservationCount', 1))
        reservation_time_str = request.args.get('reservationTime', '12:00')
        # HH:MM
        sort_type = int(request.args.get('sortType', 1))
        latitude = float(request.args['latitude'])
        longitude = float(request.args['longitude'])

        if sort_type not in self.SORT_TYPE:
            abort(400)

        time_gap_min = self._get_time_gap(reservation_time_str)
        restaurants = self._get_restaurant_objects(sector, reservation_time_str, reservation_count, time_gap_min)

        return self.unicode_safe_json_dumps(
            self._get_sorted_restaurant_list(restaurants, sort_type, latitude, longitude)
        ) if time_gap_min >= 0 else Response('', 204)


@api.resource('/restaurant/map')
class RestaurantMap(BaseResource):
    def get(self):
        """
        내 주변 식당 목록 조회
        """


@api.resource('/restaurant/<restaurant_id>')
class Restaurant(BaseResource):
    def get(self, restaurant_id):
        """
        식당 정보 조회
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
