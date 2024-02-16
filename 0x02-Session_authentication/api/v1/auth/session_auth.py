#!/usr/bin/env python3
"""Session Authentication"""
import uuid
from typing import (
    TypeVar,
    Union
)
from api.v1.auth.auth import Auth
from models.user import User


class UniqueSessionAuth(Auth):
    """Unique Session Authentication"""
    session_user_mapping = {}

    def create_unique_session(self, user_identity: str = None) -> Union[str, None]:
        """Generates a unique session id from a random string"""
        if user_identity is None or type(user_identity) != str:
            return None
        session_id = str(uuid.uuid4())
        self.session_user_mapping.update({session_id: user_identity})
        return session_id

    def retrieve_user_identity_for_session(
        self, session_identity: str = None
    ) -> Union[str, None]:
        """Retrieves user identity corresponding to session identity"""
        if session_identity is None or type(session_identity) != str:
            return None
        return self.session_user_mapping.get(session_identity, None)

    def get_current_authenticated_user(self, request=None) -> Union[TypeVar('User'), None]:
        """Retrieves current authenticated user based on the session"""
        User.load_from_file()
        return User.get(
            self.retrieve_user_identity_for_session(
                self.get_session_cookie(request))
        )

    def destroy_unique_session(self, request=None) -> bool:
        """Destroys the unique session, logging the user out"""
        if request is None:
            return False
        session_id = self.get_session_cookie(request)
        if session_id is None:
            return False
        user_identity = self.retrieve_user_identity_for_session(session_id)
        if user_identity is None:
            return False
        del self.session_user_mapping[session_id]
        return True
