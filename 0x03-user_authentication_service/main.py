#!/usr/bin/env python3
"""
test all endpoints
"""
import requests


base_url = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    check for success
    """
    url = base_url + '/users'
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    log in with wrong pass
    """
    url = base_url + '/sessions'
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    login success test
    """
    url = base_url + '/sessions'
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    return resp.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    """
    test for profile logged in
    """
    url = base_url + '/profile'
    cookies = {
        'session_id': session_id
    }
    resp = requests.get(url, cookies=cookies)
    assert resp.status_code == 200


def profile_unlogged() -> None:
    """
    test for profile logged in
    """
    url = base_url + '/profile'
    resp = requests.get(url)
    assert resp.status_code == 403


def log_out(session_id: str) -> None:
    """
    test the logout endpoint
    """
    url = base_url + '/sessions'
    cookie = {
        'session_id': session_id
    }
    resp = requests.delete(url, cookies=cookie)
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """
    test the reset password endpoint
    """
    url = base_url + '/reset_password'
    data = {'email': email}
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    test the update_password endpoint
    """
    url = base_url + '/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    resp = requests.put(url, data=data)
    assert resp.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
