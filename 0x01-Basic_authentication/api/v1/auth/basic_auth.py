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

    def decode_base64_authorization_header(self, base64_header: str) -> str:
        """
        decodes base64 string
        """
        import base64

        try:
            if type(base64_header) is str:
                msg = base64.b64decode(base64_header)
                return msg.decode('utf-8')
            return None
        except Exception:
            return None

    def extract_user_credentials(self, decoded_header: str) -> (str, str):
        """
        extracts the client's credentials
        """
        if (not decoded_header or type(decoded_header) is not str or
                ":" not in decoded_header):
            return None, None

        u_email, u_pass = decoded_header.split(':')
        return u_email, u_pass
