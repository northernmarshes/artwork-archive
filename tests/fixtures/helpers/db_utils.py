import pytest
from pathlib import Path


@pytest.fixture
def populated_database():
    """Returns a populated database"""
    return Path(__file__).parent / "fixtures" / "databases" / "populated.db"
