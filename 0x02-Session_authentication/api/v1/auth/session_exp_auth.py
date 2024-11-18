#!/usr/bin/env python3
"""SessionExpAuth"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """adds expiration date to a Sesion ID"""
    def __init__(self):
        """overloads base method"""
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """creates a session that
           expires after `session_duration`
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_id = self.user_id_by_session_id[session_id]
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns value of current_session[session_id]
        """
        session_dict = super().user_id_for_session_id(session_id)
        if not session_dict:
            return None
        user_id = session_dict.get('user_id')
        if self.session_duration <= 0:
            return user_id
        created_at = session_dict.get('created_at')
        if not created_at or created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return user_id
