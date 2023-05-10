# pybit
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Build Status](https://img.shields.io/pypi/pyversions/pybit)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/pypi/v/pybit)](https://pypi.org/project/pybit/)
[![Build Status](https://travis-ci.org/verata-veritatis/pybit.svg?branch=master)](https://travis-ci.org/verata-veritatis/pybit)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

Official Python3 API connector for Bybit's HTTP and WebSockets APIs.

## Table of Contents

- [About](#about)
- [Development](#development)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)
- [Contributors](#contributors)
- [Donations](#donations)

## About
Put simply, `pybit` (Python + Bybit) is the official lightweight one-stop-shop module for the Bybit HTTP and WebSocket APIs. Originally created by [Verata Veritatis](https://github.com/verata-veritatis), it's now maintained by Bybit employees - however, you're still welcome to contribute!

It was designed with the following vision in mind:

> I was personally never a fan of auto-generated connectors that used a mosh-pit of various modules you didn't want (sorry, `bravado`) and wanted to build my own Python3-dedicated connector with very little external resources. The goal of the connector is to provide traders and developers with an easy-to-use high-performing module that has an active issue and discussion board leading to consistent improvements.

## Development
`pybit` is being actively developed, and new Bybit API changes should arrive on `pybit` very quickly. `pybit` uses `requests` and `websocket-client` for its methods, alongside other built-in modules. Anyone is welcome to branch/fork the repository and add their own upgrades. If you think you've made substantial improvements to the module, submit a pull request and we'll gladly take a look.

## Installation
`pybit` requires Python 3.9.1 or higher. The module can be installed manually or via [PyPI](https://pypi.org/project/pybit/) with `pip`:
```
pip install git+https://github.com/burchesoka/pybit.git@v5+copytrading
```

## Usage
You can retrieve a specific market like so:
```python
from pybit.unified_trading import HTTP
```
Create an HTTP session and connect via WebSocket for Inverse on mainnet:
```python
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key='...',
    api_secret='...'
)
```
Information can be sent to, or retrieved from, the Bybit APIs:

```python
# Get orderbook.
session.orderbook(symbol='BTCUSD')

# Create five long orders.
payload = {"category": "option"}
orders = [{
  "symbol": "ETHUSDT",
  "side": "Buy",
  "orderType": "Limit",
  "qty": "0.1",
  "price": i,
} for i in [1700, 1900, 2200, 2400, 2450]]

payload["request"] = orders
# Submit the orders in bulk.
session.place_batch_order(payload)

```
Websocket for copytrading:
```python
import time
from pybit.copy_trading import WebSocket as CPWebsocket


def get_private_websocket(test: bool = False):
    if test:
        api_key = 'xxx'
        api_secret = 'xxx'
    else:
        api_key = 'xxx'
        api_secret = 'xxx'

    return CPWebsocket(
        channel_type='private',
        api_key=api_key,
        api_secret=api_secret,
        testnet=True if test else None,
        restart_on_error=True,
        retries=200,
        ping_interval=19,
    )

def main():
    def user_data_handler(message):
        print(message)

    try:
        ws_private = get_private_websocket(test=True)

        ws_private.copy_trade_order_stream(user_data_handler)

        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        ...
    except Exception as e:
        print(e)
        raise e
    finally:
        ws_private.exit()


if __name__ == '__main__':
    main()
```
Check out the example python files or the list of endpoints below for more information on available
endpoints and methods. Usage examples on the `HTTP` methods can
be found at:
- [Session examples](/examples/direct_session.py)
- [Wrapper examples](/examples/wrapper_class.py)


## Contact
You can reach out for support on the [BybitAPI Telegram](https://t.me/BybitAPI) group chat.

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/verata-veritatis"><img src="https://avatars0.githubusercontent.com/u/9677388?v=4" width="100px;" alt=""/><br /><sub><b>verata-veritatis</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=verata-veritatis" title="Code">💻</a> <a href="https://github.com/verata-veritatis/pybit/commits?author=verata-veritatis" title="Documentation">📖</a></td>
     <td align="center"><a href="https://github.com/APF20"><img src="https://avatars0.githubusercontent.com/u/74583612?v=4" width="100px;" alt=""/><br /><sub><b>APF20</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=APF20" title="Code">💻</a></td>
     <td align="center"><a href="https://github.com/cameronhh"><img src="https://avatars0.githubusercontent.com/u/30434979?v=4" width="100px;" alt=""/><br /><sub><b>Cameron Harder-Hutton</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=cameronhh" title="Code">💻</a></td>
     <td align="center"><a href="https://github.com/tomcru"><img src="https://avatars0.githubusercontent.com/u/35841182?v=4" width="100px;" alt=""/><br /><sub><b>Tom Rumpf</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=tomcru" title="Code">💻</a></td>
     <td align="center"><a href="https://github.com/tconley"><img src="https://avatars1.githubusercontent.com/u/1893207?v=4" width="100px;" alt=""/><br /><sub><b>Todd Conley</b></sub></a><br /><a href="https://github.com/tconley/pybit/commits?author=tconley" title="Ideas">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
