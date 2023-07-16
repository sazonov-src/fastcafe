import pytest

from app_order.services.new_order import update_or_create_new_order

pytestmark = [pytest.mark.django_db]


def test_create_with_count(user, menu_item, count=5):
    _, (ord_item, _) = update_or_create_new_order(user=user, item=menu_item, quantity=count)
    assert ord_item.quantity == count
    
def test_create_default_count(user, menu_item ):
    _, (ord_item, _) = update_or_create_new_order(user=user, item=menu_item)
    assert ord_item.quantity == 1

def test_create_not_correct_count(user, menu_item, count=0):
    _, (ord_item, _) = update_or_create_new_order(user=user, item=menu_item, quantity=count)
    assert ord_item.quantity == 1
 
