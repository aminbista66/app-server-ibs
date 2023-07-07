import geocoder
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, status
from rest_framework.response import Response


from inventory.models.inventory import Inventory
from inventory.models.inventory_item import InventoryItem
from inventory.models.sub_inventory import SubInventory
from inventory.models.sub_store import SubStore
from inventory.permissions.inventory_permissions import CanChangeInventoryPermission

from inventory.serializers.send_to_sub_store_serializers import SendToSubStoreSerializer
from logs.logs_mixins import CHANGE, get_client_ip
from logs.models import CustomActionLogs


class SendToSubStoreAPIView(generics.GenericAPIView):
    http_method_names = ["post"]
    serializer_class = SendToSubStoreSerializer
    permission_classes = [CanChangeInventoryPermission]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_id = serializer.validated_data["item_id"]
        sub_store_id = serializer.validated_data["sub_store_id"]
        quantity = serializer.validated_data["quantity"]

        item = InventoryItem.objects.get(id=item_id)
        inventory = Inventory.objects.get(item=item)
        sub_store = SubStore.objects.get(id=sub_store_id)

        sub_inventory: SubInventory
        try:
            sub_inventory = SubInventory.objects.get(item=item, sub_store=sub_store)
        except SubInventory.DoesNotExist:
            sub_inventory = SubInventory()
            sub_inventory.item = item
            sub_inventory.sub_store = sub_store
            sub_inventory.save()
            inventory.sub_inventories.add(sub_inventory)

        inventory.quantity -= quantity
        sub_inventory.quantity += quantity

        sub_inventory.save()
        inventory.save()

        current_time = timezone.now()
        client_ip = geocoder.ip(str(get_client_ip(request)))
        
        # logging change in inventory
        content_type = ContentType.objects.get_for_model(inventory)
        CustomActionLogs.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=inventory.id,
            object_repr="Nothing",
            action_flag=CHANGE,
            change_message=f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Updated {Inventory.__name__}",
            device_ip=get_client_ip(request),
            location=f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}",
        )

        # logging change in sub-inventory
        content_type = ContentType.objects.get_for_model(sub_inventory)
        CustomActionLogs.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=sub_inventory.id,
            object_repr="Nothing",
            action_flag=CHANGE,
            change_message=f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Updated {SubInventory.__name__}",
            device_ip=get_client_ip(request),
            location=f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}",
        )

        return Response(
            {"message": "inventory sent to sub-store successfully"},
            status=status.HTTP_200_OK,
        )
