from django.db import models
from django.db import models
from django.contrib.admin.models import LogEntry


class CustomActionLogs(LogEntry):
    device_ip = models.CharField(max_length=50)
    location = models.CharField(max_length=50, null=True)
    device_type = models.CharField(max_length=50)
    device_os = models.CharField(max_length=50)
    browser_type = models.CharField(max_length=50)
    

    def __str__(self) -> str:
        return self.device_ip
    
    class Meta:
        verbose_name = "ibs log"




