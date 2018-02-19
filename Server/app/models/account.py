from app.models import *


class UnverifiedAccountModel(Document):
    meta = {
        'collection': 'unverified_account'
    }

    email = StringField(
        primary_key=True
    )

    pw = StringField(
        required=True
    )

    verify_url = StringField(
        required=True
    )


class AccountModel(Document):
    meta = {
        'collection': 'account'
    }

    id = StringField(
        primary_key=True
    )
    # Common Account : email
    # SNS Account : Each SNS' identity

    pw = StringField()
    # Common Account : pbkdf2_hmac hashed password
    # SNS Account : None

    connected_sns = StringField()
    # Common Account : None
    # SNS Account : Connected SNS' name

    phone = StringField(
        unique=True,
        required=True
    )

    name = StringField(
        required=True
    )

    birthday = DateTimeField(
        required=True
    )

    sex = StringField(
        required=True
    )


class RefreshTokenModel(Document):
    """
    Manages JWT refresh token
    """
    meta = {
        'collection': 'refresh_token'
    }

    token = UUIDField(
        primary_key=True
    )
    token_owner = ReferenceField(
        document_type=AccountModel,
        required=True,
        reverse_delete_rule=CASCADE
    )
    pw_snapshot = StringField()
