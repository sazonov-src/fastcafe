from django.contrib import admin
from apps.order.models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Checkout)
