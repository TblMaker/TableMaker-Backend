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
        """
        - Test
        Load korean restaurant list with sort type 1

        Load chinese restaurant list with sort type 2

        Load chinese restaurant list with sort type 3

        Load chinese restaurant list with sort type 4

        - Exception Test
        Load chinese restaurant list with past reservationTime
            * Validation
            (1) status code : 204

        Load chinese restaurant list with reservationCount 999
            * Validation
            (1) status code : 200
            (2) response data type : list
            (3) length of resource : 0

        Load chinese restaurant list with sortType 99
            * Validation
            (1) status code : 400
        """
        # -- Test --
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

        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.valid_reservation_time,
            'sortType': 2,
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

        # (4)
        self.assertEqual(data[0]['name'], '맛있고 비싼 식땅')
        self.assertEqual(data[2]['name'], '맛있는 식땅')

        restaurant = data[0]
        self.assertIsInstance(restaurant, dict)

        self.assertIn('thumbnail', restaurant)
        self.assertIsNone(restaurant['thumbnail'])
        del restaurant['thumbnail']

        self.assertDictEqual(restaurant, {
            'name': '맛있고 비싼 식땅',
            'rating': 0.0,
            'distance': 1.0766231543
        })

        # ---

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

        # (4)
        self.assertEqual(data[0]['name'], '맛있고 싼 식땅')
        self.assertEqual(data[2]['name'], '맛있고 비싼 식땅')

        restaurant = data[0]
        self.assertIsInstance(restaurant, dict)

        self.assertIn('thumbnail', restaurant)
        self.assertIsNone(restaurant['thumbnail'])
        del restaurant['thumbnail']

        self.assertDictEqual(restaurant, {
            'name': '맛있고 싼 식땅',
            'rating': 0.0,
            'distance': 1.0767234142
        })

        # ---

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

        # (4)
        self.assertEqual(data[0]['name'], '맛있고 비싼 식땅')
        self.assertEqual(data[2]['name'], '맛있고 싼 식땅')

        restaurant = data[0]
        self.assertIsInstance(restaurant, dict)

        self.assertIn('thumbnail', restaurant)
        self.assertIsNone(restaurant['thumbnail'])
        del restaurant['thumbnail']

        self.assertDictEqual(restaurant, {
            'name': '맛있고 비싼 식땅',
            'rating': 0.0,
            'distance': 1.0766231543
        })
        # -- Test --

        # -- Exception Test --
        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.past_reservation_time,
            'sortType': 4,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 204)

        # ---

        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 999,
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
        self.assertEqual(len(data), 0)

        # ---

        resp = self.request(self.client.get, '/restaurant/chinese', {
            'reservationCount': 2,
            'reservationTime': self.valid_reservation_time,
            'sortType': 99,
            'latitude': self.latitude,
            'longitude': self.longitude
        })

        # (1)
        self.assertEqual(resp.status_code, 400)
        # -- Exception Test --
