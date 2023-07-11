from django.db import models

from app_order.models import Order


class PaymentCallback(models.Model):
    objects = models.Manager

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    action = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    data = models.TextField(blank=True)

