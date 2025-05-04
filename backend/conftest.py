import pytest
import os
from src.util.dao import DAO

@pytest.fixture(scope="module")
def test_dao():
    # Använd lokal MongoDB utan autentisering
    os.environ["MONGO_URL"] = "mongodb://localhost:27017"

    test_instance = DAO("todo")
    test_instance.collection.create_index("description", unique=True)
    yield test_instance
    test_instance.drop()
