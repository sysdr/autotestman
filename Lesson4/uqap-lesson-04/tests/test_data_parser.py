"""
Test suite for data parser
"""
import pytest
from pathlib import Path
from src.data_parser import load_users_csv, load_users, load_users_lazy
from src.models import UserModel


@pytest.fixture
def data_dir():
    """Path to test data directory"""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def csv_file(data_dir):
    """Path to test CSV file"""
    return data_dir / "test_users.csv"


def test_csv_parsing(csv_file):
    """Verify CSV loads correctly"""
    users = load_users_csv(csv_file)
    
    assert len(users) > 0, "Should load at least one user"
    assert all(isinstance(u, UserModel) for u in users), "All items should be UserModel objects"


def test_user_validation():
    """Test that invalid data raises errors"""
    
    # Invalid email
    with pytest.raises(ValueError, match="Invalid email"):
        UserModel(email="not-an-email", password="Pass123!", role="user", active=True)
    
    # Short password
    with pytest.raises(ValueError, match="Password too short"):
        UserModel(email="test@test.com", password="short", role="user", active=True)
    
    # Invalid role
    with pytest.raises(ValueError, match="Invalid role"):
        UserModel(email="test@test.com", password="Pass123!", role="hacker", active=True)


def test_boolean_normalization(csv_file):
    """Verify TRUE/FALSE strings convert to Python booleans"""
    users = load_users_csv(csv_file)
    
    for user in users:
        assert isinstance(user.active, bool), f"active should be bool, got {type(user.active)}"


def test_lazy_loading(csv_file):
    """Verify iterator doesn't load all into memory at once"""
    user_iter = load_users_lazy(csv_file)
    
    # Iterator should yield UserModel objects
    first_user = next(user_iter)
    assert isinstance(first_user, UserModel)


def test_universal_loader(csv_file):
    """Test auto-detection of file format"""
    users = load_users(csv_file)
    assert len(users) > 0


def test_missing_file():
    """Verify proper error when file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        load_users_csv(Path("nonexistent.csv"))


def test_user_methods():
    """Test UserModel helper methods"""
    admin = UserModel(
        email="admin@test.com",
        password="Admin123!",
        role="admin",
        active=True
    )
    
    assert admin.is_privileged() == True
    
    user_dict = admin.to_dict()
    assert user_dict['email'] == "admin@test.com"
    assert user_dict['role'] == "admin"
