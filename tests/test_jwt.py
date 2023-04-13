from simple_jwt import jwt
import base64
import json
from time import time
import pytest

param = 'eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2ODEzMzcyNTYsImlhdCI6MTY4MTMzMzY1Niwic2lkIjoiMTUzMDcxNjQyNzYiLCJhaWQiOiI4NjUyNTk4MDg1IiwiY2lkIjoiNTA0MzA3MDIiLCJ0eXBlIjoiciJ9.jmFoOydgYnL8AqmgnLSFU2l_E6q3pnPHh7ss-g7xKO7tLD_JY8vZR3O-cthNInFzi9G2M3t2boRzMTatlbsZ7Q'

@pytest.fixture
def token() -> str:
    return 'eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2ODEzMzcyNTYsImlhdCI6MTY4MTMzMzY1Niwic2lkIjoiMTUzMDcxNjQyNzYiLCJhaWQiOiI4NjUyNTk4MDg1IiwiY2lkIjoiNTA0MzA3MDIiLCJ0eXBlIjoiciJ9.jmFoOydgYnL8AqmgnLSFU2l_E6q3pnPHh7ss-g7xKO7tLD_JY8vZR3O-cthNInFzi9G2M3t2boRzMTatlbsZ7Q'
@pytest.fixture
def too_many_segments() -> str:
    return 'eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2ODEzMzcyNTYsImlhdCI6MTY4MTMzMzY1Niwic2lkIjoiMTUzMDcxNjQyNzYiLCJhaWQiOiI4NjUyNTk4MDg1IiwiY2lkIjoiNTA0MzA3MDIiLCJ0eXBlIjoiciJ9.jmFoOydgYnL8AqmgnLSFU2l_E6q3pnPHh7ss-g7xKO7tLD_JY8vZR3O-cthNInFzi9G2M3t2.boRzMTatlbsZ7Q'
@pytest.fixture
def invalid_base64() -> str:
    return 'eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2ODEzMzcyNTYsImlhdCI6MTY4MTMzMzY1Niwic2lkIjoiMTUzMDcxNjQyNzYiLCJhaWQiOiI4NjUyNTk4MDg1IiwiY2lkIjoiNTA0MzA3MDIiLCJ0eXBlIjoiciJ.jmFoOydgYnL8AqmgnLSFU2l_E6q3pnPHh7ss-g7xKO7tLD_JY8vZR3O-cthNInFzi9G2M3t2boRzMTatlbsZ7Q'

@pytest.fixture
def active_token() -> str:
    claims =  {
        "exp": int(time()) + 3600,
        "iat": int(time()),
        "sid": "15307164276",
        "aid": "8652598085",
        "cid": "50430702",
        "type": "r"
    }
    input = json.dumps(claims).encode('utf-8')
    payload = base64.urlsafe_b64encode(input)
    header = 'eyJhbGciOiJIUzUxMiJ9'
    fake_sig = 'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    active_token = f'{header}.{payload.decode()}.{fake_sig}'
    return active_token

@pytest.fixture
def bad_json_token() -> str:
    claims =  {
        "exp": int(time()) + 3600,
        "iat": int(time()),
        "sid": "15307164276",
        "aid": "8652598085",
        "cid": "50430702",
        "type": "r"
    }
    input = json.dumps(claims).encode('utf-8') + b'bad'
    payload = base64.urlsafe_b64encode(input)
    header = 'eyJhbGciOiJIUzUxMiJ9'
    fake_sig = 'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    active_token = f'{header}.{payload.decode()}.{fake_sig}'
    return active_token

def test_decode(token: str):
    decoded = jwt.decode(token)
    assert decoded['headers']['alg'] == 'HS512'
    assert decoded['claims']['exp'] == 1681337256
    assert decoded['claims']['iat'] == 1681333656
    assert decoded['claims']['sid'] == '15307164276'
    assert decoded['claims']['aid'] == '8652598085'
    assert decoded['claims']['cid'] == '50430702'
    assert decoded['claims']['type'] == 'r'
    assert decoded['signature'] == 'jmFoOydgYnL8AqmgnLSFU2l_E6q3pnPHh7ss-g7xKO7tLD_JY8vZR3O-cthNInFzi9G2M3t2boRzMTatlbsZ7Q'


def test_decode_too_many_segments(too_many_segments: str):
    with pytest.raises(ValueError):
        jwt.decode(too_many_segments)

def test_invalid_base64(invalid_base64: str):
    with pytest.raises(base64.binascii.Error):
        jwt.decode(invalid_base64)

def test_json_encoded(bad_json_token: str):
    with pytest.raises(json.JSONDecodeError):
        jwt.decode(bad_json_token)


def test_expired_token(token: str):
    assert jwt.is_expired(token)

def test_not_expired_token(active_token: str):
    assert not jwt.is_expired(active_token)


class does_not_raise:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

@pytest.mark.parametrize(
    "test_input, expected",
    [
        (123, pytest.raises(TypeError)),
        ({token: param}, pytest.raises(TypeError)),
        (param, does_not_raise()),
        (bytes(param, 'utf-8'), does_not_raise()),
    ],
)
def test_jwt_input_types(test_input, expected):
    with expected:
        jwt.decode(test_input)
