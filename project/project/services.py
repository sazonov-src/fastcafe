import abc

from django.db import models


class ServiceBase:
    model = None
    "Це базовий клас що імплементує бізнес логіку моделі"
    def __init__(self, **kwargs):
        self.m = self.model(**kwargs)

    # @classmethod
    # def create(cls, **kwargs):
    #     return cls.model(**kwargs)

    def __getattr__(self, item):
        return getattr(self.m, item)
