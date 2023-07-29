import pytest

from app_order.services.new_order import NewOrder


pytestmark = [pytest.mark.django_db]

def test_create_new_order(new_order: NewOrder, menu_item):
    order = new_order.update_or_create(menu_item)
    assert order.is_order_create is True
    assert order.is_item_create is True
    
    
def test_update_new_order(new_order: NewOrder, menu_item):
    new_order.update_or_create(menu_item)
    order = new_order.update_or_create(menu_item)
    assert order.is_order_create is False
    assert order.is_item_create is False
    
    
    
