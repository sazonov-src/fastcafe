from django.contrib import admin

from app_checkout.models import Checkout
from app_order.models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Checkout)
