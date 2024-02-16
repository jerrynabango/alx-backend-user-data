#!/usr/bin/env python3
"""Authentication"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """Authentication Management Class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Ensures authentication on every request"""
        if (
            path is None
            or excluded_paths is None
            or len(excluded_paths) == 0
        ):
            return True
        for url in excluded_paths:
            if url.endswith('*'):
                if url[:-1] in path:
                    return False
            else:
                if path in url or path + '/' in url:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Extracts Authorization Header"""
        auth = request.headers.get('Authorization', None) if request else None
        if request is None or auth is None:
            return None
        return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the currently authenticated user"""
        return None
