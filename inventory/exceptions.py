from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidSubInventory(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Given sub inventories are invalid"
    default_code = "invalid_sub_inventory"