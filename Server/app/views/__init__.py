import ujson
import time

from flask import Response, abort, request
from flask_restful import Resource


def json_required(*required_keys):
    """
    View decorator for JSON validation.
    - About custom view decorator
    -> http://flask-docs-kr.readthedocs.io/ko/latest/patterns/viewdecorators.html

    - If content-type is not application/json : returns status code 406
    - If required_keys are not exist on request.json : returns status code 400

    :type required_keys: str
    """
    def decorator(fn):
        if fn.__name__ == 'get':
            print('[WARN] JSON with GET method? on "{}()"'.format(fn.__qualname__))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(406)

            for required_key in required_keys:
                if required_key not in request.json:
                    abort(400)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


class BaseResource(Resource):
    """
    BaseResource with some helper functions based flask_restful.Resource
    """
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_response(cls, data, status_code=200):
        """
        Helper function which processes json response with unicode using ujson

        - About ujson.dumps(data, ensure_ascii=False)
        If ensure_ascii is true (the default),
        all non-ASCII characters in the output are escaped with \\uXXXX sequences,
        and the result is a str instance consisting of ASCII characters only.

        If ensure_ascii is false, some chunks written to fp may be unicode instances.

        :type data: dict or list
        :type status_code: int

        :rtype: Response
        """
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8'
        )


class Router(object):
    """
    REST resource routing helper class like standard flask 3-rd party libraries
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Routes resources. Use app.register_blueprint() aggressively

        :type app: Flask
        """
