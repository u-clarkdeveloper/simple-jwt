from __future__ import annotations

import subprocess
import sys
from unittest.mock import patch

import pytest
from simple_jwt import cli


@pytest.fixture
def token() -> str:
    return 'eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2ODEzMzcyNTYsImlhdCI6MTY4MTMzMzY1Niwic2lkIjoiMTUzMDcxNjQyNzYiLCJhaWQiOiI4NjUyNTk4MDg1IiwiY2lkIjoiNTA0MzA3MDIiLCJ0eXBlIjoiciJ9.jmFoOydgYnL8AqmgnLSFU2l_E6q3pnPHh7ss-g7xKO7tLD_JY8vZR3O-cthNInFzi9G2M3t2boRzMTatlbsZ7Q'


def test_format_json():
    data = {'test': 'value', 'nested': {'key': 'value'}}
    formatted = cli.format_json(data)
    assert '{\n  "test": "value",' in formatted
    assert '"nested": {\n    "key": "value"\n  }' in formatted


def test_main_success(token, capsys):
    with patch('sys.argv', ['jwt', token]):
        exit_code = cli.main()
        captured = capsys.readouterr()
        
        assert exit_code == 0
        assert 'Decoded JWT Token:' in captured.out
        assert '"alg": "HS512"' in captured.out
        assert '"exp": 1681337256' in captured.out
        assert 'Token Status: EXPIRED' in captured.out


def test_main_with_raw_option(token, capsys):
    with patch('sys.argv', ['jwt', token, '--raw']):
        exit_code = cli.main()
        captured = capsys.readouterr()
        
        assert exit_code == 0
        assert 'Decoded JWT Token:' not in captured.out
        assert '"headers": {' in captured.out
        assert '"claims": {' in captured.out
        assert '"signature":' in captured.out


def test_main_with_check_expiry_option(token, capsys):
    with patch('sys.argv', ['jwt', token, '--check-expiry']):
        exit_code = cli.main()
        captured = capsys.readouterr()
        
        assert exit_code == 0
        assert 'Token Status: EXPIRED' in captured.out


def test_main_error_invalid_token(capsys):
    with patch('sys.argv', ['jwt', 'invalid_token']):
        exit_code = cli.main()
        captured = capsys.readouterr()
        
        assert exit_code == 1
        assert 'Error decoding token:' in captured.err 