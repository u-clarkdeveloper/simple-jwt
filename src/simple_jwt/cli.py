#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from simple_jwt import jwt


def format_json(data: Dict[str, Any]) -> str:
    """Format JSON data for pretty printing."""
    return json.dumps(data, indent=2)


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Decode and validate JWT tokens',
        prog='jwt',
    )
    parser.add_argument(
        'token',
        help='JWT token to decode',
    )
    parser.add_argument(
        '--check-expiry',
        '-e',
        action='store_true',
        help='Check if the token is expired',
    )
    parser.add_argument(
        '--raw',
        '-r',
        action='store_true',
        help='Print raw decoded data without formatting',
    )

    args = parser.parse_args()

    try:
        decoded = jwt.decode(args.token)
        
        if not args.raw:
            print("Decoded JWT Token:")
            print(f"Header: {format_json(decoded['headers'])}")
            print(f"Claims: {format_json(decoded['claims'])}")
            print(f"Signature: {decoded['signature']}")
        else:
            print(format_json(decoded))
        
        if args.check_expiry or not args.raw:
            is_expired = jwt.is_expired(args.token)
            print(f"\nToken Status: {'EXPIRED' if is_expired else 'ACTIVE'}")
        
        return 0
    except Exception as e:
        print(f"Error decoding token: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main()) 