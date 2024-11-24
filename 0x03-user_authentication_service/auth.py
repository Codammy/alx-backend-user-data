#!/usr/bin/env python3
"""user authentication module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """encrypts str password and return bytes password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)
