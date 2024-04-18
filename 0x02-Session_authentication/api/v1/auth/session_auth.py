#!/usr/bin/env python3
"""
session auth implementaion
"""
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    template for session auth
    """
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a Session_id for user Id
        """
        from uuid import uuid4

        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a user_id based on a session_id
        """
        if type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id:
            return user_id
        return None

    def current_user(self, request=None):
        """
        retrieves current user from the database
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is not None:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """
        destroy/ logout a session
        """
        from api.v1.app import auth

        if request is None:
            return False
        session_id = auth.session_cookie(request)
        if not session_id:
            return False
        if self.user_id_for_session_id(session_id):
            del self.user_id_by_session_id[session_id]
            return True
        return False
