#!/usr/bin/env python3
"""
Auth implementation
"""
from db import DB
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


def _hash_password(password: str) -> bytes:
    """
    hash password using bcrypt
    """
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt()
    )
    return hashed_password


def _generate_uuid() -> str:
    """generate unique id"""
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth():
    """
    Auth class to interact with the authentication db
    """
    def __init__(self):
        """
        create a db instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register_user but check if user exists first
        """
        if type(email) is not str or type(password) is not str:
            raise ValueError
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        created a session for user login
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None
        except ValueError:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """retrieves user using the session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """deletes session_id from db"""
        if type(user_id) is not int:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate reset token for password
        """
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError("no result found")

    def update_password(self, reset_token, new_password):
        """update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(new_password)
            user.reset_token = None
            user.session_id = None
        except NoResultFound:
            raise(ValueError)
