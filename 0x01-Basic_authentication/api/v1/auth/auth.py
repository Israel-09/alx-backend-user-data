#!/usr/bin/env python3
"""authentication template
"""
from typing import List, TypeVar


class Auth:
    """Autication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if session requires auth"""
        req_auth = True
        if not path or (not excluded_paths or len(excluded_paths) == 0):
            return True

        path = path.rstrip('/') + '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                req_auth = not path.startswith(excluded_path.rstrip('*'))
            else:
                req_auth = not path == excluded_path
            if req_auth is False:
                return req_auth
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
