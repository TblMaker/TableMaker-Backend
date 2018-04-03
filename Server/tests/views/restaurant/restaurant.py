from datetime import datetime, timedelta

from app.models.restaurant import RestaurantModel

from tests.views import TCBase


class TestRestaurantList(TCBase):
    """
    TC about

    This TC tests
        * GET /restaurant/<sector>
    """
    def setUp(self):
        """
        - Before Test

        Upload restaurants
            * POST /restaurant/<sector>
        """
        super(TestRestaurantList, self).setUp()

        # ---

        self.valid_reservation_time = str((datetime.now() + timedelta(minutes=11)).time())[:5]
        self.past_reservation_time = str((datetime.now() + timedelta(minutes=-1)).time())[:5]
        self.latitude = 36.636733
        self.longitude = 127.097428

        self.json_request(self.client.post, '/restaurant/chinese', {
            'name': '맛있는 식땅',
            'tel': '111-1111-1111',
            'priceAvg': 8000,
            'latitude': 36.635733,
            'longitude': 127.085428,
            'address': '대전광역시 유성구 가정북로 뭐시기',
            'openTime': '09:00',
            'closeTime': '21:00',
            'closeDays': [0, 6],
            'minReservationCount': 2,
            'maxReservationCount': 20,
            'reservationGapMinutes': 10
        })

        self.json_request(self.client.post, '/restaurant/chinese', {
            'name': '맛있고 싼 식땅',
            'tel': '111-1111-1111',
            'priceAvg': 6000,
            'latitude': 36.635734,
            'longitude': 127.085429,
            'address': '대전광역시 유성구 가정북로 뭐시기',
            'openTime': '09:00',
            'closeTime': '21:00',
            'closeDays': [0, 6],
            'minReservationCount': 2,
            'maxReservationCount': 20,
            'reservationGapMinutes': 10
        })

        self.json_request(self.client.post, '/restaurant/chinese', {
            'name': '맛있고 비싼 식땅',
            'tel': '111-1111-1111',
            'priceAvg': 9000,
            'latitude': 36.635735,
            'longitude': 127.085430,
            'address': '대전광역시 유성구 가정북로 뭐시기',
            'openTime': '09:00',
            'closeTime': '21:00',
            'closeDays': [0, 6],
            'minReservationCount': 2,
            'maxReservationCount': 20,
            'reservationGapMinutes': 10
        })

    def tearDown(self):
        """
        - After Test
        """
        RestaurantModel.objects.delete()

        # ---

        super(TestRestaurantList, self).tearDown()

    def test(self):
        # -- Test --

        # 데이터베이스에는 없는 한국 식당 조회
        resp = self.request(self.client.get, '/restaurant/korean', {
            'reservationCount': 2,
            'reservationTime': self.valid_reservation_time,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 200)

        # (2)
        data = self.get_response_data(resp)
        self.assertIsInstance(data, list)

        # (3)
        self.assertEqual(len(data), 0)

        # ---

        # 중식당을 sort type 2로 조회(가까운 거리 ~ 먼 거리)
        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.valid_reservation_time,
            'sortType': 2,
            'latitude': self.latitude,
            'longitude': self.longitude,
        })

        # (1)
        self.assertEqual(resp.status_code, 200)

        # (2)
        data = self.get_response_data(resp)
        self.assertIsInstance(data, list)

        # (3)
        self.assertEqual(len(data), 3)

        # (4) 거리 측정
        current_restaurant_distance = 0
        for restaurant in data:
            self.assertLessEqual(current_restaurant_distance, restaurant['distance'])
            current_restaurant_distance = restaurant['distance']

        # ---

        # 중식당을 sort type 3으로 조회(낮은 가격 ~ 높은 가격)
        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.valid_reservation_time,
            'sortType': 3,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 200)

        # (2)
        data = self.get_response_data(resp)
        self.assertIsInstance(data, list)

        # (3)
        self.assertEqual(len(data), 3)

        # (4) 가격 측정(목록 API에선 price avg를 반환하지 않으므로 음식점 이름으로 테스트)
        self.assertEqual(data[0]['name'], '맛있고 싼 식땅')
        self.assertEqual(data[2]['name'], '맛있고 비싼 식땅')

        # ---

        # 중식당을 sort type 4로 조회(높은 가격 ~ 낮은 가격)
        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.valid_reservation_time,
            'sortType': 4,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 200)

        # (2)
        data = self.get_response_data(resp)
        self.assertIsInstance(data, list)

        # (3)
        self.assertEqual(len(data), 3)

        # (4) 가격 측정(목록 API에선 price avg를 반환하지 않으므로 음식점 이름으로 테스트)
        self.assertEqual(data[0]['name'], '맛있고 비싼 식땅')
        self.assertEqual(data[2]['name'], '맛있고 싼 식땅')

        # ---

        # 중식당을 sort type 5와 page 2로 조회(Pagination이 제대로 되었는지 검사)
        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.valid_reservation_time,
            'sortType': 5,
            'page': 2,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 200)

        # (2)
        data = self.get_response_data(resp)
        self.assertIsInstance(data, list)

        # (3) 2페이지에는 음식점이 없어야 함
        self.assertEqual(len(data), 0)
        # -- Test --

        # -- Exception Test --

        # 예약 시간이 과거
        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.past_reservation_time,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 204)

        # ---

        # 맞는 식당이 없는 예약 인원
        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 999,
            'reservationTime': self.valid_reservation_time,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 200)

        # (2)
        data = self.get_response_data(resp)
        self.assertIsInstance(data, list)

        # (3)
        self.assertEqual(len(data), 0)
        # -- Exception Test --
