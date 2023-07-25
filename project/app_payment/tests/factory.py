from app_checkout.factory import ChackoutFactory
from app_payment.services import NewPayment


class PeymentFactory:
    def __init__(self, user, menu_item):
        self._checkout_factory = ChackoutFactory(user=user, menu_item=menu_item)
        self._payment = NewPayment(user=user)

    def __getattr__(self, name):
        return getattr(self._payment, name)
