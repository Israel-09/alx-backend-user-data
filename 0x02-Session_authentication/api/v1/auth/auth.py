#!/usr/bin/env python3
"""authentication template
"""
from typing import List, TypeVar
from os import getenv
from flask import jsonify


class Auth:
    """Autication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if session requires auth"""
        if not path or (not excluded_paths or len(excluded_paths) == 0):
            return True

        path = path.rstrip('/') + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        headers = request.headers
        if request is None or 'Authorization' not in headers:
            return None
        return headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """
        gets a cookie value from a request
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        print(session_name)
        return request.cookies.get(session_name)
