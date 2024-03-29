from django.http.response import Http404
import pytest
from app_order.models import OrderItem

from app_order.services.new_order import NewOrder

pytestmark = [pytest.mark.django_db]


def test_delete_order_with_one_item(new_order: NewOrder, menu_item):
    new_order.update_or_create(menu_item)
    order_item = OrderItem.objects.get(item=menu_item)
    assert new_order.delete(order_item) == 2
    with pytest.raises(Http404):
        new_order()
    
    
def test_delete_only_item(new_order: NewOrder, menu_item, an_menu_item):
    new_order.update_or_create(menu_item)
    new_order.update_or_create(an_menu_item)
    order_item = OrderItem.objects.get(item=menu_item)
    assert new_order.delete(order_item) == 1
    new_order()
