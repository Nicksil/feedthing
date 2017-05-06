from rest_framework.exceptions import APIException


class ResourceDoesNotExist(APIException):
    status_code = 404
