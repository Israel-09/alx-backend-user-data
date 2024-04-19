#!/usr/bin/env python3
"""
basic auth implementation
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


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
        if type(decoded_header) is not str or ":" not in decoded_header:
            return None, None
        u_email, u_pass = decoded_header.split(':')
        return u_email, u_pass

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """get user from credentials"""
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        user = User.search({"email": user_email})
        if user:
            user = user[0]
            if user.is_valid_password(user_pwd) is True:
                return user
            else:
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves current user from db"""
        if not request:
            return None
        auth_header = self.authorization_header(request)
        b64credentials = self.extract_base64_authorization_header(auth_header)
        credentials = self.decode_base64_authorization_header(b64credentials)
        mail_pass = self.extract_user_credentials(credentials)
        if mail_pass:
            u_email, u_pass = mail_pass
            return self.user_object_from_credentials(u_email, u_pass)
        return None
