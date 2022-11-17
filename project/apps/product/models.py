from django.db import models

class Product(models.Model):
    """Цей клас містить загальні дані про товар"""
    title = models.CharField(max_length=255, verbose_name='Назва')
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name='Категорія')
    description = models.TextField(verbose_name='Опис')
    photo = models.ImageField(upload_to='product/', verbose_name='Зображення')
    is_publish = models.BooleanField(default=True, verbose_name='Опубліковано?')
    is_delivery = models.BooleanField(default=True, verbose_name='Є доставка?')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункти меню'


class ProductChild(models.Model):
    """Розширює Product більш конкретними даними"""
    subtitle = models.CharField(max_length=255, verbose_name='Назва')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name='Товар')
    price = models.IntegerField(verbose_name='Ціна')
    photo = models.ImageField(upload_to='product_child/', verbose_name='Зображення')

    def __str__(self):
        return self.subtitle

    class Meta:
        verbose_name = 'Підпункт меню'
        verbose_name_plural = 'Підпункти меню'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    photo = models.ImageField(upload_to='category/', verbose_name='Зображення')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
