from app_order.services.new_order import update_or_create_new_order
import pytest


pytestmark = [pytest.mark.django_db]

@pytest.mark.django_db
def test_create_order(user, menu_item):
    update_or_create_new_order(user=user, item=menu_item)



    
