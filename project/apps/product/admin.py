from django.contrib import admin
from apps.product.models import *

admin.site.register(Product)
admin.site.register(ProductChild)
admin.site.register(Category)
