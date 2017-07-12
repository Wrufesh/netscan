from django.db import models

# Create your models here.
from netscan.utils.fields import MACAddressField


class MyAccessPoint(models.Model):
    bssid = MACAddressField()
    ssid = models.CharField(max_length=200, null=True, blank=True)
    channel = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.ssid) + str(self.bssid)

