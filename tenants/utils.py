import re

from .models import Tenant

def hostname_from_request(request):
    try:
        regex = re.compile("^HTTP_")
        new_dict = dict(
            (regex.sub("", header), value)
            for (header, value) in request.META.items()
            if header.startswith("HTTP_")
        )
        domain = (new_dict["ORIGIN"]).split("://")[1].lower()

        return domain
    except KeyError:
        return request.get_host().lower()


def tenant_db_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    print("DB to use:", tenants_map.get(hostname))
    return tenants_map.get(hostname)


def get_tenants_map():
    # tenant_map = {"test.localhost:8000": "test"}
    tenant_map = dict(Tenant.objects.using('default').values_list("subdomain", "schema_name"))
    print("tenant map:", tenant_map)
    return tenant_map
