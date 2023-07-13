from django.contrib.auth.models import User
import pytest

from mixer.backend.django import mixer
# from project.test.mixer import mixer


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user():
    return mixer.blend(User)


@pytest.fixture
def another_user():
    return mixer.blend(User)


@pytest.fixture
def menu_item():
    return mixer.blend("app_menu.menuitem")




