import pytest
from django.core.cache import cache


pytest_plugins = [
    "project.fixtures",
    "app_order.fixtures"
]


@pytest.fixture(autouse=True)
def _cache(request):
    """Clear django cache after each test run."""
    yield
    cache.clear()
