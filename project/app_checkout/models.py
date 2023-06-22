from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField

from app_order.models import Order


class Checkout(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    phone = PhoneNumberField(region='UA')
    cart_pay = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.order} - {self.user_name}'
