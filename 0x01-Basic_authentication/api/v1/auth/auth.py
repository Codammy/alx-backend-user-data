#!/usr/bin/env python3
"""
auth module containing auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """API authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns false"""
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get currents user object"""
        return None
