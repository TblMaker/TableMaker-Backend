RESTAURANT_LIST_GET = {
    'tags': ['음식점 정보'],
    'description': '음식점 목록 조회',
    'parameters': [
        {
            'name': 'sector',
            'description': '음식점 종류(선호메뉴)\n'
                           '음식 종류가 "아무거나"일 경우 "all"',
            'in': 'path',
            'type': 'str',
            'required': True
        },
        {
            'name': 'reservationCount',
            'description': '예약 인원 수\n'
                           '기본값: 1',
            'in': 'query',
            'type': 'int',
            'required': False
        },
        {
            'name': 'reservationTime',
            'description': '예약 시간(hh:mm)\n'
                           '기본값: 12:00',
            'in': 'query',
            'type': 'str',
            'required': False
        },
        # {
        #     'name': 'priceLevel',
        #     'description': '가격대\n'
        #                    '1: 저렴\n'
        #                    '2: 보통\n'
        #                    '3: 기분',
        #     'in': 'query',
        #     'type': 'int',
        #     'required': True
        # },
        {
            'name': 'latitude',
            'description': '위도',
            'in': 'query',
            'type': 'float',
            'required': True
        },
        {
            'name': 'longitude',
            'description': '경도',
            'in': 'query',
            'type': 'float',
            'required': True
        },
        {
            'name': 'sortType',
            'description': '정렬 기준\n'
                           '1: 예약 인기 높은순(기본값)\n'
                           '2: 거리순(가까운 거리부터)\n'
                           '3: 가격순(저 -> 고)\n'
                           '4: 가격순(고 -> 저)\n'
                           '5 이상: 평점순(고 -> 저)',
            'in': 'query',
            'type': 'int',
            'required': False
        },
        {
            'name': 'page',
            'description': '음식점을 5개 단위로 pagination하기 위함\n'
                           '기본값: 1',
            'in': 'query',
            'type': 'int',
            'required': False
        }
    ],
    'responses': {
        '200': {
            'description': '목록 조회 성공',
            'examples': {
                '': [
                    {
                        'name': '맛있고 비싼 식땅',
                        'rating': 4.0,
                        'distance': 1.0766231543,
                        'thumbnail': None
                    },
                    {
                        'name': '맛있고 싼 식땅',
                        'rating': 3.8,
                        'distance': 1.0767234142,
                        'thumbnail': None
                    },
                    {
                        'name': '맛있는 식땅',
                        'rating': 4.2,
                        'distance': 1.0768236836,
                        'thumbnail': '1e3b75c9eea13.png'
                    }
                ]
            }
        },
        '204': {
            'description': '목록 조회 실패(예약 시간이 현재보다 과거)'
        }
    }
}

RESTAURANT_LIST_POST = {
    'tags': ['음식점 정보'],
    'description': '새로운 음식점 추가',
    'parameters': [
        {
            'name': 'sector',
            'description': '음식점 종류',
            'in': 'path',
            'type': 'str',
            'required': True
        },
        {
            'name': 'name',
            'description': '음식점 이름',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'priceAvg',
            'description': '1인당 평균 가격',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'latitude',
            'description': '음식점 위도',
            'in': 'json',
            'type': 'float',
            'required': True
        },
        {
            'name': 'longitude',
            'description': '음식점 경도',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'address',
            'description': '음식점 주소',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'openTime',
            'description': '음식점 여는 시간(HH:MM)',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'closeTime',
            'description': '음식점 닫는 시간(HH:MM)',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'closeDays',
            'description': '음식점 휴무일(0: 일요일, 1: 월요일, ..., 6: 토요일)\n'
                           'ex) [0, 5, 6]',
            'in': 'json',
            'type': 'list',
            'required': True
        },
        {
            'name': 'minReservationCount',
            'description': '최소 예약 인원',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'maxReservationCount',
            'description': '최대 예약 인원',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'reservationGapMinutes',
            'description': '예약을 위한 최소 텀(분)',
            'in': 'json',
            'type': 'int',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': '음식점 추가 성공'
        }
    }
}
