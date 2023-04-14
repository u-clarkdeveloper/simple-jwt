from __future__ import annotations

import base64
import binascii
import json
from time import time


def decode(token: str | bytes) -> dict:
    """Decode a JWT token.

    Args:
        token (str | bytes): The token to decode.

    Returns:
        dict: The decoded token without the verification of signature.
    """
    if isinstance(token, bytes):
        token = token.decode()
    if not isinstance(token, str):
        raise TypeError('Invalid token: token must be a string or bytes')

    try:
        headers, claims, signature = token.split('.')
    except ValueError:
        raise ValueError(
            "Invalid token: token must have 3 parts separated by '.'",
        )

    try:
        header_decoded = base64.b64decode(headers)
        claims_decoded = base64.b64decode(claims)
    except binascii.Error:
        raise binascii.Error(
            'Invalid token: token must be base64 encoded',
        )

    # try:
    header_data = json.loads(header_decoded)
    claims_data = json.loads(claims_decoded)
    # except json.JSONDecodeError:
    # print("Invalid token: token must be json encoded")

    return {'headers': header_data, 'claims': claims_data, 'signature': signature}


def is_expired(token: str | bytes) -> bool:
    """Check if a JWT token is expired.

    Args:
        token (str | bytes): The token to check.

    Returns:
        bool: True if the token is expired, False otherwise.
    """
    decoded = decode(token)
    return decoded['claims']['exp'] < time()
