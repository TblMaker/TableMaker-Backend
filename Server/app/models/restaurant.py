from bson.objectid import ObjectId

from app.models import *


class RestaurantModel(Document):
    meta = {
        'collection': 'restaurant'
    }

    name = StringField(
        required=True
    )

    sector = StringField(
        required=True
    )
    # Fast food, Korean food, Japanese food, ...

    tel = StringField(
        required=True
    )

    thumbnail_image_name = StringField(
        required=True
    )

    latitude = FloatField(
        required=True
    )
    longitude = FloatField(
        required=True
    )

    open_time = StringField(
        required=True
    )
    close_time = StringField(
        required=True
    )
    # hh:mm:ss

    close_day = IntField(
        required=True
    )
    # Sunday: 0, Monday: 1, Tuesday: 2, ..., Saturday: 6

    price_range = StringField(
        required=True
    )
    # \d+~\d+

    min_reservation_count = IntField(
        required=True
    )
    max_reservation_count = IntField(
        required=True
    )

    reservation_gap_minutes = IntField(
        required=True
    )

    rating = FloatField(
        required=True
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
