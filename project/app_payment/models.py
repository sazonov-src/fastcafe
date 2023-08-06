from django.db import models

from app_order.models import Order


class PayCallback(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    is_payed = models.BooleanField()
