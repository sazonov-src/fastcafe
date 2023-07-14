import pytest
from app_order.services.new_order import update_or_create_new_order

pytestmark = [pytest.mark.django_db]

def test_update_new_order(user, menu_item, an_menu_item):
    (order, _), (order_item, _) = update_or_create_new_order(user=user, item=menu_item)
    (an_order, _), (an_order_item, _) = update_or_create_new_order(user=user, item=an_menu_item)
    assert order.pk == an_order.pk
    assert order_item.pk != an_order_item.pk
    
    
def test_enother_user(user, another_user, menu_item):
    (order, _), (order_item, _) = update_or_create_new_order(user=user, item=menu_item)
    (an_order, _), (an_order_item, _) = update_or_create_new_order(
        user=another_user, item=menu_item)
    assert order.pk != an_order.pk
    assert order_item.pk != an_order_item.pk
