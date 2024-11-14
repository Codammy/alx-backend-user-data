#!/usr/bin/env python3
"""Basic auth"""

from api.v1.auth import Auth


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
