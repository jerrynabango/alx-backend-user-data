#!/usr/bin/env python3
"""Passoword hashing & bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check password validity"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
