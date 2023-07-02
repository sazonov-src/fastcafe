from django.db import models


class MenuItemGeneral(models.Model):
    """Цей клас містить загальні дані про товар"""
    title = models.CharField(max_length=255, verbose_name='Назва')
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name='Категорія')
    description = models.TextField(verbose_name='Опис')
    photo = models.ImageField(upload_to='app_menu/', blank=True, verbose_name='Зображення')
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано?')

    def __str__(self):
        return f"<{self.title}>"

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункти меню'


class MenuItem(models.Model):
    """Розширює MenuItemGeneral більш конкретними даними"""
    subtitle = models.CharField(max_length=255, verbose_name='Назва')
    menu_item = models.ForeignKey(
        MenuItemGeneral, on_delete=models.PROTECT, verbose_name='Товар')
    price = models.IntegerField(verbose_name='Ціна')
    photo = models.ImageField(upload_to='menu_item/', blank=True, verbose_name='Зображення')
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано?')

    @property
    def title(self):
        return f"{self.menu_item.title} {self.subtitle}"

    def __str__(self):
        return f'{self.menu_item} {self.subtitle}'

    class Meta:
        verbose_name = 'Підпункт меню'
        verbose_name_plural = 'Підпункти меню'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    photo = models.ImageField(upload_to='category/', blank=True, verbose_name='Зображення')
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано?')

    def __str__(self):
        return f"<{self.title}>"

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


def get_test_item(num=1):
    category = Category.objects.create(title='категорія')
    menu_item = MenuItemGeneral.objects.create(title='тестовий item',
                                               category=category,
                                               description='опис')
    return MenuItem.objects.create(subtitle='Test Item' + str(num),
                                   menu_item=menu_item,
                                   price=25)
