import pytest
from pymongo.errors import WriteError

def test_insert_valid_todo(test_dao):
    # Test inserting a valid todo item
    todo = {"description": "Clean the kitchen", "done": False}
    result = test_dao.create(todo)
    assert result["description"] == "Clean the kitchen"
    assert result["done"] is False
    assert "_id" in result

def test_insert_without_required_field(test_dao):
    # Missing 'description' field, should fail
    incomplete = {"done": True}
    with pytest.raises(WriteError):
        test_dao.create(incomplete)

def test_insert_with_wrong_type(test_dao):
    # 'done' should be a boolean, not a string
    invalid = {"description": "Wrong type", "done": "yes"}
    with pytest.raises(WriteError):
        test_dao.create(invalid)

def test_insert_duplicate_description(test_dao):
    # Two items with same description – unique index violation
    unique_item = {"description": "Non-duplicate", "done": False}
    test_dao.create(unique_item)
    with pytest.raises(WriteError):
        test_dao.create({"description": "Non-duplicate", "done": True})

def test_insert_with_extra_field_allowed(test_dao):
    # Adding a property that is not in the schema – should be accepted
    data = {"description": "Includes extras", "done": False, "priority": "high"}
    result = test_dao.create(data)
    assert result["priority"] == "high"
