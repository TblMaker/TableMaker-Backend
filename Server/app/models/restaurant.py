from app.models import *


class RestaurantModel(Document):
    meta = {
        'collection': 'restaurant'
    }

    id = SequenceField(
        primary_key=True
    )

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
