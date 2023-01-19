from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from apps.menu.models import MenuItemChild


class UserAuthenticatedError(Exception):
    ...


class OrderManager(models.Manager):

    def get_or_create_order(self, user: User):
        if user.is_anonymous:
            raise UserAuthenticatedError('Користувач не авторизований')
        return self.get_or_create(user=user, status='new')

    def get_order(self, user):
        return self.get_or_create_order(user)[0]

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

    objects = OrderManager()

    def __str__(self):
        return f'{self.user} - {self.status}'

    def __iter__(self):
        return iter(self.orderitem_set.all())

    @property
    def order_items(self):
        return self.orderitem_set.all()

    @property
    def total_price(self):
        return sum(order_item.total_price for order_item in self)

    def del_item(self, item: MenuItemChild):
        if item in self.orderitem_set.all():
            return self.orderitem_set.get(item=item).delete()

    def add_item(self, item: MenuItemChild, quantity: int):
        self.orderitem_set.update_or_create(
            item=item,
            defaults={'quantity': quantity if quantity > 0 else 1}
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item: MenuItemChild = models.ForeignKey(MenuItemChild, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.order}: <{self.item} * {self.quantity} = {self.total_price}>'

    @property
    def total_price(self):
        return self.item.price * self.quantity

    def plus_quantity(self):
        self.quantity += 1
        self.save()

    def minus_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()


class Checkout(models.Model):
    pass
