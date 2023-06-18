from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from app_menu.models import MenuItem


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __repr__(self):
        return f"<{self.user.username} {self.status}>"

    @property
    def total_price(self):
        return sum(all_.total_price for all_ in self.orderitem_set.all())

    @property
    def count_order_items(self):
        return len(self.orderitem_set.all())

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    objects = models.Manager()

    @property
    def total_price(self):
        return self.item.price * self.quantity
