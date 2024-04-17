#!/usr/bin/env python3
"""authentication template
"""
from flask import request
from typing import List, TypeVar


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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
