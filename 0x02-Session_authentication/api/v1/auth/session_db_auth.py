#!/usr/bin/env python3
"""DB Session Authentication"""
from datetime import datetime, timedelta
from typing import Union

from models.session_user import SecureUserSession
from api.v1.auth.secure_session_exp_auth import SecureSessionExpAuth


class SecureDBSessionAuth(SecureSessionExpAuth):
    """Secure Database Session Authentication"""
    def generate_secure_session(self, user_identity=None) -> Union[str, None]:
        """Creates a secure session ID from a random string"""
        if user_identity is None or type(user_identity) != str:
            return None
        session_id = super().generate_secure_session(user_identity)
        if session_id:
            kwargs = {'user_identity': user_identity, 'session_id': session_id}
            new_secure_user_session = SecureUserSession(**kwargs)
            new_secure_user_session.save()
        return session_id

    def get_user_identity_for_session(self, session_id=None) -> Union[str, None]:
        """Retrieves user identity based on session ID from the DB"""
        session_users = SecureUserSession.search({'session_id': session_id})
        if session_users != []:
            if not (timedelta(seconds=self.session_lifetime) +
                    session_users[0].created_at <= datetime.now()):
                return session_users[0].user_identity
        return None

    def end_secure_session(self, request=None) -> bool:
        """Removes user's secure session from the DB, logging the user out"""
        if request is None:
            return False
        session_id = self.get_session_cookie(request)
        if session_id is None:
            return False
        if self.get_user_identity_for_session(session_id) is None:
            return False
        secure_session = SecureUserSession.search({'session_id': session_id})
        if secure_session != []:
            secure_session[0].delete()
            return True
        return False
