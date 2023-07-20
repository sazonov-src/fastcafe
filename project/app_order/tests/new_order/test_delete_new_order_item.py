import pytest

from app_order.services.new_order import delete_new_order_item

pytestmark = [pytest.mark.django_db]

def test_delete_order_with_one_item(order_with_one_item):
    order_item = order_with_one_item.orderitem_set.first()
    delete_new_order_item(order_item=order_item)
    with pytest.raises(ValueError):
        # ValueError: 'Order' instance needs to have a primary key 
        # value before this relationship can be use
        order_with_one_item.orderitem_set.first() 

def test_delete_order_with_two_items(order_with_two_items):
    order_item = order_with_two_items.orderitem_set.first()
    delete_new_order_item(order_item=order_item)
    order_with_two_items.orderitem_set.first()
