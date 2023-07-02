from django.db import models

from app_order.models import Order


class PaymentCallback(models.Model):
    objects = models.Manager

    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    action: str = models.CharField(max_length=255, blank=True)
    status: str = models.CharField(max_length=255, blank=True)
    data: str = models.TextField(blank=True)

