from django.contrib import admin
from apps.menu.models import *

admin.site.register(MenuItem)
admin.site.register(MenuItemChild)
admin.site.register(Category)
