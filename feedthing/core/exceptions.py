from rest_framework import status
from rest_framework.exceptions import APIException


class FeedManagerError(Exception):
    """An error during FeedManager execution."""
    pass


class ResourceDoesNotExist(APIException):
    default_detail = 'Resource does not exist.'
    status_code = status.HTTP_404_NOT_FOUND
