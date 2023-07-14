
from mixer.backend.django import mixer


def factory():
    return mixer.blend("app_order.orderitem")
