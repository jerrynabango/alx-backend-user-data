#!/usr/bin/env python3
"""user sessions"""
from datetime import datetime
from models.base import Base


class UserSession(Base):
    """Custom user session management class"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a new instance of User Session"""
        super().__init__(*args, **kwargs)
        self.custom_user_id = kwargs.get('custom_user_id')
        self.custom_session_id = kwargs.get('custom_session_id')
        self.custom_created_at = datetime.now()
