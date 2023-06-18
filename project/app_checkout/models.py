from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField

from app_order.models import Order


class Checkout(models.Model):

    PAYMENT_CHOICES = (
        ('card', 'Оплата картою'),
        ('on_receipt', 'При отриманні')
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    phone = PhoneNumberField(region='UA')
    payment = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.order} - {self.user_name}'
