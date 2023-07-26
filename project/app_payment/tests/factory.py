from app_checkout.factory import ChackoutFactory
from app_payment.services import NewPayment


class PeymentFactory:
    def __init__(self, user, menu_item):
        self._user = user
        self._checkout_factory = ChackoutFactory(user=user, menu_item=menu_item)
        self._payment = NewPayment(user=user)

    def __getattr__(self, name):
        return getattr(self._payment, name)

    def checkout(self):
        self._checkout_factory.create_new_checkout(
            user_name="Vasia",
            phone="+380987775544")
        self._checkout_factory.create_new_order()
        self._payment = NewPayment(user=self._user)
