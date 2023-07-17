import pytest
from project.tests.mixer import mixer as _mixer

@pytest.fixture
def mixer():
    return _mixer
