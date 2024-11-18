#!/usr/bin/env python3
"""
SessionDBAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    Class for SessionDBAuth
    """
    def create_session(self, user_id=None):
        """creates and stores new instance of
           UserSession and returns the Session ID
        """
        if not user_id:
            return None
        session_id = super().create_session(user_id=user_id)
        UserSession({session_id: user_id}).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting
            UserSession in the database based on session_id
        """
        user_id = super().user_id_for_session_id(session_id)
        if not user_id:
            return None
        return UserSession.get(session_id)

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the
            Session ID from the request cookie
        """
        session_id = request.cookies.get(getenv('SESSION_NAME'))
        user_session = self.user_id_for_session_id(session_id)
        user_session.remove()
        # return super().destroy_session(request)
