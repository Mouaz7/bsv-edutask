import pytest
from src.controllers.usercontroller import UserController

# Simulated user object for test purposes
class MockUser:
    def __init__(self, email):
        self.email = email

# Fake DAO implementation to simulate database behavior
@pytest.fixture
def mock_user_dao():
    class MockDAO:
        def __init__(self):
            self.query_log = []
            self.fake_data = []

        def find(self, query):
            self.query_log.append(query)
            return self.fake_data

    return MockDAO()

# Test that a single matching user is correctly returned
def test_finds_single_user_by_email(mock_user_dao):
    user = MockUser("valid@example.com")
    mock_user_dao.fake_data = [user]
    controller = UserController(dao=mock_user_dao)
    result = controller.get_user_by_email("valid@example.com")
    assert result is user
    assert mock_user_dao.query_log == [{"email": "valid@example.com"}]

# Test that None is returned if no matching user is found
def test_returns_none_when_no_user_found(mock_user_dao):
    mock_user_dao.fake_data = []
    controller = UserController(dao=mock_user_dao)
    result = controller.get_user_by_email("missing@example.com")
    assert result is None

# Test that a warning is printed and the first user is returned if multiple matches are found
def test_logs_when_multiple_users_found(mock_user_dao, capsys):
    user1 = MockUser("duplicate@example.com")
    user2 = MockUser("duplicate@example.com")
    mock_user_dao.fake_data = [user1, user2]
    controller = UserController(dao=mock_user_dao)
    result = controller.get_user_by_email("duplicate@example.com")
    logs = capsys.readouterr()
    assert "more than one user found with mail duplicate@example.com" in logs.out
    assert result is user1

# Test that an invalid email without '@' raises ValueError
def test_raises_error_for_invalid_email_format(mock_user_dao):
    controller = UserController(dao=mock_user_dao)
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email.com")

# Test that an empty email string raises ValueError
def test_raises_error_for_empty_email(mock_user_dao):
    controller = UserController(dao=mock_user_dao)
    with pytest.raises(ValueError):
        controller.get_user_by_email("")

# Test that an exception from DAO is propagated
def test_propagates_exception_from_dao(mock_user_dao):
    def crashing_find(query):
        raise RuntimeError("Simulated DB failure")

    mock_user_dao.find = crashing_find
    controller = UserController(dao=mock_user_dao)
    with pytest.raises(RuntimeError) as error_info:
        controller.get_user_by_email("fail@example.com")

    assert "Simulated DB failure" in str(error_info.value)
