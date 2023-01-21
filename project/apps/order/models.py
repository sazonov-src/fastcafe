from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from apps.menu.models import MenuItemChild
from phone_field import PhoneField


class UserAuthenticatedError(Exception):
    ...


class OrderQueryset(models.QuerySet):

    def get_or_create(self, defaults=None, **kwargs):
        user = kwargs.get('user')
        if not user:
            raise ValueError('user обовязковий аргумент')
        if user.is_anonymous:
            raise UserAuthenticatedError('Користувач не авторизований')
        return super().get_or_create(defaults=None, status='new', user=user, **kwargs)

    def create(self, user: User, **kwargs):
        return self.get_or_create(user=user)[0]


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

    objects = OrderQueryset.as_manager()

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
    phone = PhoneField()
    delivery = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    payment = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    