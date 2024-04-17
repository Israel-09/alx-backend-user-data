#!/usr/bin/env python3
"""
basic auth implementation
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth template"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base 64 from the header"""
        if type(authorization_header) is str:
            if authorization_header.startswith('Basic '):
                return authorization_header.split()[1]
        return None
