#!/usr/bin/env python3
"""Basic auth"""

from api.v1.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication"""

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """extracts base64 authorization header"""
        if not authorization_header or type(authorization_header) is not str\
                or not authorization_header.startswith('Basic'):
            return None
        login = authorization_header.strip()[6:]
        return login

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """decodes base 64 string"""
        if not base64_authorization_header or\
                type(base64_authorization_header) is not str:
            return None
        decoded_login: str
        try:
            decoded_login = base64.b64decode(base64_authorization_header)
        except Exception as e:
            return None
        return decoded_login.decode()

    def extract_user_credentials(self, decoded_base64_authorization_header)\
            -> (str, str):
        """returns user credentials from based on decoded auth header"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """returns User instance based on his email and password"""
        users = None
        if not user_email or type(user_email) is not str:
            return users
        if not user_pwd or type(user_pwd) is not str:
            return users
        try:
            users = User.search({"email": user_email})
        except Exception as e:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        authorization = self.authorization_header(request)
        encoded_credentials = self.extract_base64_authorization_header(authorization)
        decoded_credentials = self.decode_base64_authorization_header(encoded_credentials)
        email, passwd = self.extract_user_credentials(decoded_credentials)
        return self.user_object_from_credentials(email, passwd)
