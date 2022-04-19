import pytest

from utils.quantities import PhysicalQuantity

@pytest.fixture
def q():
    return PhysicalQuantity()

class TestPhysicalQuantity:
    pass