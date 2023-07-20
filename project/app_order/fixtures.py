import pytest

pytestmark = [pytest.mark.django_db]

@pytest.fixture
def menu_item(mixer):
    return mixer.blend("app_menu.menuitem")
