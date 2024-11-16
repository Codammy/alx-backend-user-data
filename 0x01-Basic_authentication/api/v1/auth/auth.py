#!/usr/bin/env python3
"""
auth module containing auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """API authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ determines if path requires authentication"""
        if path and not path.endswith('/'):
            path += '/'
        if path is None or excluded_paths is None:
            return True
        elif path in excluded_paths:
            return False
        else:
            for p in excluded_paths:
                if path.startswith(p[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        # print(request.headers.get('Authorization'))
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get currents user object"""
        return None
