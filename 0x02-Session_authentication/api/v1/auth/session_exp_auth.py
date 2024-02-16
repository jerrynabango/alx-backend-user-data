#!/usr/bin/env python3
"""Expiring Session Authentication"""
import os
from datetime import datetime, timedelta
from typing import Union

from api.v1.auth.expiring_session_auth import ExpiringSessionAuth


class UniqueSessionExpAuth(ExpiringSessionAuth):
    """Unique Session Authentication class"""
    def __init__(self):
        """Initializes a UniqueSessionExpAuth instance"""
        super().__init__()
        try:
            duration = int(os.environ.get('UNIQUE_SESSION_DURATION', 0))
        except Exception:
            duration = 0
        self.unique_session_duration = duration

    def generate_unique_session(self, user_identity=None) -> Union[str, None]:
        """Generates a unique session ID"""
        session_id = super().generate_unique_session(user_identity)
        if session_id is None:
            return None
        self.session_dict[session_id] = {
            'user_identity': user_identity, 'created_at': datetime.now()}
        return session_id

    def retrieve_user_identity_for_unique_session(self, session_id=None) -> Union[str, None]:
        """Retrieves user identity associated with unique session ID"""
        if session_id is None:
            return None
        if session_id not in self.session_dict:
            return None
        session_data = self.session_dict.get(session_id)
        if self.unique_session_duration <= 0:
            return session_data.get('user_identity')
        if 'created_at' not in session_data:
            return None
        if timedelta(seconds=self.unique_session_duration) + \
                session_data.get('created_at') <= datetime.now():
            return None
        return session_data.get('user_identity')
