from app_order.models import Order, OrderItem
from app_order.services.new_order import update_or_create_new_order
import pytest


pytestmark = [pytest.mark.django_db]


def test_create_order(user, menu_item):
    (order, _), (order_item, _) = update_or_create_new_order(user=user, item=menu_item)
    assert type(order) == Order
    assert type(order_item) == OrderItem

def test_is_cteated(user, menu_item):
    (_, ord_is_create), (_, ordi_is_create) = update_or_create_new_order(user=user, item=menu_item)
    assert ord_is_create is True
    assert ordi_is_create is True
    
def test_create_with_count(user, menu_item, count=5):
    _, (ord_item, _) = update_or_create_new_order(user=user, item=menu_item, quantity=count)
    assert ord_item.quantity == count
    
def test_create_default_count(user, menu_item ):
    _, (ord_item, _) = update_or_create_new_order(user=user, item=menu_item)
    assert ord_item.quantity == 1

