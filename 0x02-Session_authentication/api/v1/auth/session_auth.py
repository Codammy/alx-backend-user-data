#!/usr/bin/env python3
"""Session authentication
"""

from api.v1.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None)\
            -> str:
        """creates and store a user session using their id"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
