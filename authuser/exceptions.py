from rest_framework.exceptions import APIException
from rest_framework import status

class RefreshTokenExpired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Refresh token already expired."
    default_code = "expired_refresh_token"


class InvalidTokenType(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Refresh token is invalid."
    default_code = "invalid_refresh_token"