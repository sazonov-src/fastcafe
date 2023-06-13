from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.utils.model_meta import FieldInfo
from app_menu.models import MenuItemChild, MenuItem, Category
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('done', 'Done'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __repr__(self):
        return f"<{self.user.username} {self.status}>"

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItemChild, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    objects = models.Manager()


class Checkout(models.Model):
    DELIVERY_CHOICES = (
        ('pickup', 'Самовивіз'),
        ('cafe', 'Доставка кафе')
    )
    PAYMENT_CHOICES = (
        ('card', 'Оплата картою'),
        ('on_receipt', 'При отриманні')
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    phone = PhoneNumberField()
    delivery = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    payment = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.order} - {self.user_name}'
