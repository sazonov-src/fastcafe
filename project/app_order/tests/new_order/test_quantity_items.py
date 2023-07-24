import pytest

from app_order.services.new_order import NewOrder

pytestmark = [pytest.mark.django_db]


def test_create_with_count(new_order: NewOrder, menu_item, count=5):
    order = new_order.update_or_create(menu_item, quantity=count)
    assert order.item.quantity == count
    
def test_create_default_count(new_order, menu_item ):
    order = new_order.update_or_create(menu_item)
    assert order.item.quantity == 1

def test_create_not_correct_count(new_order, menu_item, count=0):
    order = new_order.update_or_create(menu_item, quantity=count)
    assert order.item.quantity == 1
 
