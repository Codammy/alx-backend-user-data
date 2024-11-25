#!/usr/bin/env python3
"""user authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """encrypts str password and return bytes password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """instantiate class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """creates a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        if type(password) is not bytes:
            password = _hash_password(password)
        return self._db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """validates user login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if not bcrypt.checkpw(password.encode(), user.hashed_password):
                return False
        except NoResultFound:
            return False
        return True
