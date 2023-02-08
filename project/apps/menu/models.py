from django.db import models

class MenuItem(models.Model):
    """Цей клас містить загальні дані про товар"""
    title = models.CharField(max_length=255, verbose_name='Назва')
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name='Категорія')
    description = models.TextField(verbose_name='Опис')
    photo = models.ImageField(upload_to='menu/', blank=True, verbose_name='Зображення')
    is_publish = models.BooleanField(default=True, verbose_name='Опубліковано?')
    is_delivery = models.BooleanField(default=True, verbose_name='Є доставка?')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункти меню'


class MenuItemChild(models.Model):
    """Розширює MenuItem більш конкретними даними"""
    subtitle = models.CharField(max_length=255, verbose_name='Назва')
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.PROTECT, verbose_name='Товар')
    price = models.IntegerField(verbose_name='Ціна')
    photo = models.ImageField(upload_to='menu_item_child/', blank=True, verbose_name='Зображення')

    def __str__(self):
        return f'{self.menu_item} {self.subtitle}'

    class Meta:
        verbose_name = 'Підпункт меню'
        verbose_name_plural = 'Підпункти меню'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    photo = models.ImageField(upload_to='category/', blank=True, verbose_name='Зображення')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


def get_test_item(num=1):
    category = Category.objects.create(title='категорія')
    menu_item = MenuItem.objects.create(title='тестовий item',
                                        category=category,
                                        description='опис')
    return MenuItemChild.objects.create(subtitle='Test Item'+str(num),
                                                 menu_item=menu_item,
                                                 price=25)
