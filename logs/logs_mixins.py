import geocoder

from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, status
from rest_framework.response import Response


from django.utils import timezone
from .models import CustomActionLogs


ADDITION = 1
CHANGE = 2
DELETION = 3

ACTION_FLAG_CHOICES = (
    (ADDITION, "Addition"),
    (CHANGE, "Change"),
    (DELETION, "Deletion"),
)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = request.META.get("REMOTE_ADDR")
    return ip


class CustomCreateAPIView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        headers = self.get_success_headers(serializer.data)
        client_ip = geocoder.ip(str(get_client_ip(request)))
        current_time = timezone.now()
        content_type = ContentType.objects.get_for_model(obj.__class__)
        CustomActionLogs.objects.create(
            user = request.user,
            content_type = content_type,
            object_id = obj.id,
            object_repr = "Nothing",
            action_flag = ADDITION,
            change_message = f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Created {obj.__class__.__name__}",

            device_ip=get_client_ip(request),
            location= f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
        )
        return Response({"message": content_type.name.capitalize() + " created successfully", "result": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class CustomUpdateAPIView(generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        current_time = timezone.now()
        client_ip = geocoder.ip(str(get_client_ip(request)))
        content_type = ContentType.objects.get_for_model(instance.__class__)
        CustomActionLogs.objects.create(
            user = request.user,
            content_type = content_type,
            object_id = instance.id,
            object_repr = "Nothing",
            action_flag = CHANGE,
            change_message = f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Updated {instance.__class__.__name__} to {instance.name if hasattr(instance, 'name') else ''}",

            device_ip=get_client_ip(request),
            location= f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
        )
        return Response({"message": content_type.name.capitalize() + " updated successfully", "result": serializer.data}, status=status.HTTP_200_OK)


class CustomDeleteAPIView(generics.DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        current_time = timezone.now()
        client_ip = geocoder.ip(str(get_client_ip(request)))
        content_type = ContentType.objects.get_for_model(instance.__class__)
        CustomActionLogs.objects.create(
            user = request.user,
            content_type = content_type,
            object_id = instance.id,
            object_repr = "Nothing",
            action_flag = DELETION,
            change_message = f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Deleted {instance.__class__.__name__} {instance.name if hasattr(instance, 'name') else ''}",

            device_ip=get_client_ip(request),
            location= f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
        )

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)



class CustomRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return Response(
            {
                "message:": content_type.name.capitalize() + " retrieved successfully",
                "result": serializer.data
            }
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        current_time = timezone.now()
        client_ip = geocoder.ip(str(get_client_ip(request)))
        content_type = ContentType.objects.get_for_model(instance.__class__)
        CustomActionLogs.objects.create(
            user = request.user,
            content_type = content_type,
            object_id = instance.id,
            object_repr = "Nothing",
            action_flag = CHANGE,
            change_message = f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Updated {instance.__class__.__name__} {instance.name if hasattr(instance, 'name') else ''}",

            device_ip=get_client_ip(request),
            location= f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
        )
        return Response({ "message": content_type.name.capitalize() + " updated successfully",  "result": serializer.data}, status=status.HTTP_200_OK)


class CustomRetrieveDeleteAPIView(generics.RetrieveDestroyAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return Response(
            {
                "message:": content_type.name.capitalize() + " retrieved successfully",
                "result": serializer.data
            }
        )
    
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        current_time = timezone.now()
        client_ip = geocoder.ip(str(get_client_ip(request)))
        CustomActionLogs.objects.create(
            user = request.user,
            content_type = ContentType.objects.get_for_model(instance.__class__),
            object_id = instance.id,
            object_repr = "Nothing",
            action_flag = DELETION,
            change_message = f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Deleted {instance.__class__.__name__} -> {instance.name if hasattr(instance, 'name') else ''}",

            device_ip=get_client_ip(request),
            location= f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
        )

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)



class CustomRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return Response(
            {
                "message:": content_type.name.capitalize() + " retrieved successfully",
                "result": serializer.data
            }
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        current_time = timezone.now()
        client_ip = geocoder.ip(str(get_client_ip(request)))
        content_type = ContentType.objects.get_for_model(instance.__class__)
        CustomActionLogs.objects.create(
            user = request.user,
            content_type = content_type,
            object_id = instance.id,
            object_repr = "Nothing",
            action_flag = CHANGE,
            change_message = f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Updated {instance.__class__.__name__} -> {instance.name if hasattr(instance, 'name') else ''}",

            device_ip=get_client_ip(request),
            location= f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
        )
        return Response({"message": content_type.name.capitalize() + " updated successfully",  "result": serializer.data }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        current_time = timezone.now()
        client_ip = geocoder.ip(str(get_client_ip(request)))
        CustomActionLogs.objects.create(
            user = request.user,
            content_type = ContentType.objects.get_for_model(instance.__class__),
            object_id = instance.id,
            object_repr = "Nothing",
            action_flag = DELETION,
            change_message = f"ON {current_time} from IP address {get_client_ip(request)} user {request.user} Deleted {instance.__class__.__name__} -> {instance.name if hasattr(instance, 'name') else ''}",

            device_ip=get_client_ip(request),
            location= f"{client_ip.city}, {client_ip.state}, {client_ip.country}",
            device_type=f"{request.user_agent.device.family}/{request.user_agent.device.brand}/{request.user_agent.device.model}",
            device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
            browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
        )

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
