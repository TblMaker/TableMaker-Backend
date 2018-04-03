RESTAURANT_LIST_GET = {
    'tags': ['식당 정보'],
    'description': '식당 목록 조회',
    'parameters': [
        {
            'name': 'sector',
            'description': '식당 종류(선호메뉴)\n'
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
            'name': 'sortType',
            'description': '정렬 기준\n'
                           '1: 예약 인기 높은순(기본값)\n'
                           '2: 거리순(가까운 거리부터)\n'
                           '3: 가격순(저 -> 고)\n'
                           '4: 가격순(고 -> 저)\n'
                           '5: 평점순(높은 평점부터)',
            'in': 'query',
            'type': 'int',
            'required': False
        },
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
