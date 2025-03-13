# Simple JWT
[![PyPI version](https://badge.fury.io/py/simple-jwt-decode.svg)](https://badge.fury.io/py/simple-jwt-decode)

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
    - [CLI Usage](#cli-usage)
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

### CLI Usage

You can also use the command-line interface to decode JWT tokens:

```console
jwt <token>
```

This will display the decoded token headers, claims, and signature, as well as whether the token is expired.

Options:
- `--check-expiry` or `-e`: Only check if the token is expired
- `--raw` or `-r`: Print raw decoded data without formatting

Example:
```console
jwt <token>
```

## License

`simple-jwt` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
