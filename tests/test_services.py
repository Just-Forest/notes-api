import pytest

from src.services.auth import AuthService
from src.services.exceptions import AlreadyExists, InvalidCredentials


def test_duplicate_signup_raises(session):
    service = AuthService(session)
    service.signup("dupe", "Testpass123")

    with pytest.raises(AlreadyExists):
        service.signup("dupe", "Testpass123")


def test_refresh_unknown_user_raises(session):
    service = AuthService(session)

    with pytest.raises(InvalidCredentials):
        service.refresh(99999)
