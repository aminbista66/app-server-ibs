from rest_framework import exceptions, status

class InternalServerError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An internal server error occurred"
    default_code = "server_error"
