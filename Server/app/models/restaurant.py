from bson.objectid import ObjectId

from app.models import *


class RestaurantModel(Document):
    meta = {
        'collection': 'restaurant'
    }

    class BasicInfo(EmbeddedDocument):
        name = StringField(
            required=True
        )

        sector = StringField(
            required=True
        )
        # Fast food, Korean food, Japanese food, ...

        tel = StringField(
            required=True,
            regex='\d+-\d+-\d+'
        )

        thumbnail_image_name = StringField(
            required=True
        )

        price_range = StringField(
            required=True,
            regex='\d+~\d+'
        )
        # 가격대

        rating = FloatField(
            required=True,
            min_value=0.0,
            max_value=5.0
        )

    basic_info = EmbeddedDocumentField(
        document_type=BasicInfo
    )

    class AddressInfo(EmbeddedDocument):
        latitude = FloatField(
            required=True
        )
        longitude = FloatField(
            required=True
        )
        # 위도, 경도

        address = StringField(
            required=True
        )
        # 주소(human readable)

    address = EmbeddedDocumentField(
        document_type=AddressInfo
    )

    class WorkingTimeInfo(EmbeddedDocument):
        open_time = DateTimeField(
            required=True
        )
        close_time = DateTimeField(
            required=True
        )
        # 영업시간(hh:mm:ss)

        close_days = ListField(
            required=True
        )
        # 휴무일(일요일 0, 월요일 1, ..., 토요일 6)

    working_time = EmbeddedDocumentField(
        document_type=WorkingTimeInfo
    )

    class ReservationInfo(EmbeddedDocument):
        min_reservation_count = IntField(
            required=True
        )
        max_reservation_count = IntField(
            required=True
        )

        reservation_gap_minutes = IntField(
            required=True
        )

    reservation = EmbeddedDocumentField(
        document_type=ReservationInfo
    )


class MenuModel(Document):
    meta = {
        'collection': 'menu'
    }

    class OptionGroup(EmbeddedDocument):
        class Option(EmbeddedDocument):
            id = ObjectIdField(
                primary_key=True,
                default=ObjectId()
            )

            title = StringField(
                required=True
            )

            price = IntField(
                required=True
            )

            countable = BooleanField(
                required=True
            )

        id = ObjectIdField(
            primary_key=True,
            default=ObjectId()
        )

        title = StringField(
            required=True
        )
        # 수량, Hot/Ice, 시럽 선택 등

        type = StringField(
            required=True
        )
        # except : counter, alternative(양자택일), radio(택일), checkbox(택다)

        options = EmbeddedDocumentListField(
            document_type=Option,
            required=True
        )

    assigned_restaurant = ReferenceField(
        document_type=RestaurantModel,
        required=True
    )

    name = StringField(
        required=True
    )

    description = StringField(
        required=True
    )

    prices = DictField(
        required=True
    )
    """
    {
        'S': 9000,
        'L': 11000
    }
    """

    options = EmbeddedDocumentListField(
        document_type=OptionGroup,
        required=True
    )
