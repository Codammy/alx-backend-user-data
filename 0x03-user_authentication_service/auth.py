#!/usr/bin/env python3
"""user authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """encrypts str password and return bytes password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def _generate_uuid() -> str:
    """returns a representation of a new UUID"""
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """creates and stores a user session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user by sesion id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str):
        """destroys current user session"""
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except Exception:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """returns user password reset token"""
        reset_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        return reset_token

    def update_password(self, reset_token: str, password: str):
        """updates user password based on reset_token validity"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=password,
                                 reset_token=None
                                 )
        except NoResultFound:
            raise ValueError
