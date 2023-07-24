import pytest

pytestmark = [pytest.mark.django_db]

@pytest.fixture
def user(mixer):
    return mixer.blend("auth.user")


@pytest.fixture
def an_user(mixer):
    return mixer.blend("auth.user")

