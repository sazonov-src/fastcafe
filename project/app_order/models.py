from typing import Any
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from app_menu.models import MenuItem


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    objects = models.Manager()
    orderitem_set: Any
    
    def __repr__(self):
        return f"<{self.user.username}>"

    @property
    def order_items(self):
        return self.orderitem_set.all()

    @property
    def total_price(self):
        return sum(all_.total_price for all_ in self.order_items)

    @property
    def count_order_items(self):
        return len(self.order_items)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    objects = models.Manager()

    @property
    def total_price(self):
        return self.item.price * self.quantity
