"""
utils/auth_service.py
Mock authentication service for lesson demonstration.
Simulates: registration, login, failed-attempt tracking, account locking.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field


MAX_ATTEMPTS = 3
LOCKOUT_SECONDS = 900  # 15 minutes in production; 0 in tests (instant)


class AuthError(Exception):
    pass


@dataclass
class UserRecord:
    username: str
    password_hash: str
    failed_attempts: int = 0
    locked_until: float = 0.0


class AuthService:
    def __init__(self) -> None:
        self._users: dict[str, UserRecord] = {}
        self._healthy: bool = True

    def is_healthy(self) -> bool:
        return self._healthy

    def register(self, username: str, password: str) -> None:
        if username in self._users:
            return  # idempotent
        self._users[username] = UserRecord(
            username=username,
            password_hash=self._hash(password),
        )

    def login(self, username: str, password: str) -> dict:
        if not password:
            raise AuthError("Password is required.")

        if username not in self._users:
            raise AuthError("Invalid credentials. Please try again.")

        record = self._users[username]

        # Check lock
        if record.locked_until > time.time():
            raise AuthError("Account locked. Try again in 15 minutes.")

        # Validate password
        if record.password_hash != self._hash(password):
            record.failed_attempts += 1
            if record.failed_attempts >= MAX_ATTEMPTS:
                record.locked_until = time.time() + 1  # 1 sec lock in test mode
                raise AuthError("Invalid credentials. Please try again.")
            raise AuthError("Invalid credentials. Please try again.")

        # Success — reset counter
        record.failed_attempts = 0
        return {
            "redirect": "/dashboard",
            "welcome": f"Welcome, {username}",
        }

    @staticmethod
    def _hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
