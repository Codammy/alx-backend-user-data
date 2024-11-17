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
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user id using it session_id as key"""
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
