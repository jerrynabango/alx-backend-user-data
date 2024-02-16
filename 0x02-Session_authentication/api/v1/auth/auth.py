#!/usr/bin/env python3
"""Custom Authentication Module"""
import os
from flask import request
from typing import List, TypeVar, Union

class CustomAuthentication:
    """Custom Authentication Class"""
    def require_authentication(self, resource_path: str, excluded_paths_list: List[str]) -> bool:
        """Requires authentication for resource access"""
        if resource_path is None or excluded_paths_list is None or not excluded_paths_list:
            return True
        for excluded_url in excluded_paths_list:
            if excluded_url.endswith('*'):
                if excluded_url[:-1] in resource_path:
                    return False
            elif resource_path in excluded_url or resource_path + '/' in excluded_url:
                return False
        return True

    def extract_authorization_header(self, http_request=None) -> Union[str, None]:
        """Extracts Authorization header from HTTP request"""
        if not http_request:
            return None
        return http_request.headers.get('Authorization', None)

    def get_current_user(self, http_request=None) -> Union[TypeVar('User'), None]:
        """Retrieves the currently logged-in user"""
        return None

    def fetch_session_cookie(self, http_request=None) -> Union[str, None]:
        """Fetches session cookie from the HTTP request"""
        if not http_request:
            return None
        cookie_name = os.getenv('CUSTOM_SESSION_NAME')
        return http_request.cookies.get(cookie_name)
