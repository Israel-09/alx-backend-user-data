#!/usr/bin/env python3
"""
Auth implementation
"""
from db import DB
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import bytes

def _hash_password(password: str) -> bytes:
    """
    hash password using bcrypt
    """
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt()
    )
    return hashed_password


class Auth():
    """
    Auth class to interact with the authentication db
    """
    def __init__(self):
        """
        create a db instance
        """
        self._db = DB()

    def register_user(self, email, password):
        """
        register_user but check if user exists first
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            self._db.add_user(email, hashed_password)

    def valid_login(self, email, password):
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

    def create_session(self, email):
        """
        created a session for user login
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid4())
            user.session_id = session_id
            self._db.commit()
            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """retrieves user using the session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound as e:
            return None

    def destroy_session(self, user_id):
        """deletes session_id from db"""
        if type(user_id) is not int:
            return
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate reset token for password
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid4())
            user.reset_token = reset_token
            self._db.commit()
            return reset_token
        except NoResultFound:
            raise ValueError("no result found")

    def update_password(self, reset_token, new_password):
        """update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(new_password)
            user.reset_token = None
            user.session_id = None
            print(user)
            self._db.commit()
        except NoResultFound:
            raise(ValueError)
