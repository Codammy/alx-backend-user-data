#!/usr/bin/env python3
"""Basic auth"""

from api.v1.auth import Auth
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
