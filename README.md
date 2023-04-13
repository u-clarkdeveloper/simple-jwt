# Simple JWT

[![PyPI - Version](https://img.shields.io/pypi/v/simple-jwt.svg)](https://pypi.org/project/simple-jwt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple-jwt.svg)](https://pypi.org/project/simple-jwt)

-----

## Why?

I created this package because I found that I often needed to see the cliams of a JWT token and wether it was expired or not. I didn't need to verify it the signatures. I wanted a package to check if the token was expired, so I could refresh my token or take other actions based off that. Most other packages seemed to require verified signatures or would throw errors if a key was not provided. Just needed a simple package to get the cliams info and if the token was expired. Simple JWT.

**Table of Contents**

- [Simple JWT](#simple-jwt)
  - [Why?](#why)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Decode](#decode)
    - [Expired](#expired)
  - [License](#license)

## Installation

```console
pip install simple-jwt-decode
```

## Usage

### Decode
```console
from simple_jwt import jwt

jwt.decode(token)
```

Should return at dict that looks similar to the following:

```
{'headers': {'alg': 'HS512'}, 'claims': {'exp': 1681337256, 'iat': 1681333656, 'sid': '15307164276', 'aid': '8652598085', 'cid': '50430702', 'type': 'r'}, 'signature': 'jmFoOydgYnL8AqmgnLSFU2l_E6q3pnPHh7ss-g7xKO7tLD_JY8vZR3O-cthNInFzi9G2M3t2boRzMTatlbsZ7Q'}
```
### Expired

```console
from simple_jwt import jwt
expired = jwt.is_expired(token)

if (expired):
    print('Your JWT token is expired! Oh no! Better get a new one')
else:
    print('Your JWT token is not expired; No need to refesh at the moment')
```

## License

`simple-jwt` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
