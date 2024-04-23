#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from time import sleep

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

session_id = auth.create_session(email)

user = auth.get_user_from_session_id(session_id)
print(user)

print(user.hashed_password)
reset_token = auth.get_reset_password_token(user.email)


password = "MyPwdBOBO"

print(user.hashed_password)
auth.update_password(reset_token, password)
print(user.hashed_password)
