#!/usr/bin/env python3
"""Basic Authorization"""
import base64
from typing import Tuple, TypeVar, Union

from api.v1.auth.auth import Auth
from api.v1.views.users import User


class CustomBasicAuth(Auth):
    """Custom Basic Authentication"""
    def extract_base64_auth_header_value(
        self, auth_header: str
    ) -> str:
        """Extracts value from Authorization value"""
        if (
            auth_header is None
            or type(auth_header) != str
            or not auth_header.startswith('Basic ')
        ):
            return None
        return ''.join(auth_header.split('Basic ')[1:])

    def decode_base64_auth_header(
        self, base64_header: str
    ) -> str:
        """Decodes base64 Authorization"""
        if (
            base64_header is None
            or type(base64_header) != str
        ):
            return None
        try:
            decoded = base64.b64decode(base64_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_credentials(
        self, decoded_auth_header: str
    ) -> Tuple[str]:
        """Extracts credentials"""
        if (
            decoded_auth_header is None
            or type(decoded_auth_header) != str
            or ":" not in decoded_auth_header
        ):
            return None, None
        credentials = decoded_auth_header.split(':')
        return credentials[0], ':'.join(credentials[1:])

    def get_user_from_credentials(
        self, email: str, password: str
    ) -> Union[TypeVar('User'), None]:
        """Get User"""
        if (
            email is None or type(email) != str
            or password is None or type(password) != str
        ):
            return None
        User.load_from_file()
        if User.count() > 0:
            users = User.search({'email': email})
            for user in users:
                if user.is_valid_password(password):
                    return user
        return None

    def fetch_current_user(self, request=None) -> TypeVar('User'):
        """Fetches current_user"""
        email, password = self.extract_credentials(
            self.decode_base64_auth_header(
                self.extract_base64_auth_header_value(
                    self.authorization_header(request=request)))
        )
        return self.get_user_from_credentials(email, password)
