from dataclasses import dataclass
from pybit.exceptions import (
    InvalidChannelTypeError,
    TopicMismatchError,
    UnauthorizedExceptionError,
)
from ._v5_market import MarketHTTP
from ._v5_trade import TradeHTTP
from ._v5_account import AccountHTTP
from ._v5_asset import AssetHTTP
from ._v5_position import PositionHTTP
from ._v5_spot_leverage_token import SpotLeverageHTTP
from ._v5_spot_margin_trade import SpotMarginTradeHTTP
from ._v5_user import UserHTTP
from ._websocket_stream import _V5WebSocketManager


WSS_NAME = "Pybit_copytrading_v3_WS"
PRIVATE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/realtime_private"
PUBLIC_SPOT = "wss://{SUBDOMAIN}.{DOMAIN}.com/usdt/public/v3"
AVAILABLE_CHANNEL_TYPES = [
    "private",
]


@dataclass
class HTTP(
    MarketHTTP,
    TradeHTTP,
    AccountHTTP,
    AssetHTTP,
    PositionHTTP,
    SpotLeverageHTTP,
    SpotMarginTradeHTTP,
    UserHTTP,
):
    def __init__(self, **args):
        super().__init__(**args)


class WebSocket(_V5WebSocketManager):
    def _validate_topic_match(self):
        if not self.WS_URL.endswith("private"):
            raise TopicMismatchError(
                "Requested topic does not match channel type"
            )

    def __init__(
        self,
        channel_type: str,
        **kwargs,
    ):
        super().__init__(WSS_NAME, **kwargs)
        if channel_type not in AVAILABLE_CHANNEL_TYPES:
            raise InvalidChannelTypeError(
                f"Channel type is not correct. Available: {AVAILABLE_CHANNEL_TYPES}"
            )
        self.WS_URL = f"{PUBLIC_SPOT}/{channel_type}"

        if channel_type == "private":
            self.WS_URL = PRIVATE_WSS

        if (
            self.api_key == None or self.api_secret == None
        ) and channel_type == "private":
            raise UnauthorizedExceptionError(
                "API_KEY or API_SECRT is not set. They both are needed in order to access private topics"
            )

        self._connect(self.WS_URL)

    # Private topics

    def copy_trade_position_stream(self, callback):
        """Subscribe to the position stream to see changes to your position data in real-time.

        Push frequency: real-time

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/private/position
        """
        self._validate_topic_match()
        topic = "copyTradePosition"
        self.subscribe(topic, callback)

    def copy_trade_order_stream(self, callback):
        """Subscribe to the order stream to see changes to your orders in real-time.

        Push frequency: real-time

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/private/order
        """
        self._validate_topic_match()
        topic = "copyTradeOrder"
        self.subscribe(topic, callback)

    def copy_trade_execution_stream(self, callback):
        """Subscribe to the execution stream to see your executions in real-time.

        Push frequency: real-time

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/private/execution
        """
        self._validate_topic_match()
        topic = "copyTradeExecution"
        self.subscribe(topic, callback)

    def copy_trade_wallet_stream(self, callback):
        """Subscribe to the wallet stream to see changes to your wallet in real-time.

        Push frequency: real-time

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/private/wallet
        """
        self._validate_topic_match()
        topic = "copyTradeWallet"
        self.subscribe(topic, callback)

    # def greek_stream(self, callback):
    #     """Subscribe to the greeks stream to see changes to your greeks data in real-time. option only.
    #
    #     Push frequency: real-time
    #
    #     Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/private/greek
    #     """
    #     self._validate_topic_match()
    #     topic = "greeks"
    #     self.subscribe(topic, callback)
    #
    # # Public topics
    #
    # def orderbook_stream(self, depth: int, symbol: str, callback):
    #     """Subscribe to the orderbook stream. Supports different depths.
    #
    #     Linear & inverse:
    #     Level 1 data, push frequency: 10ms
    #     Level 50 data, push frequency: 20ms
    #     Level 200 data, push frequency: 100ms
    #     Level 500 data, push frequency: 100ms
    #
    #     Spot:
    #     Level 1 data, push frequency: 10ms
    #     Level 50 data, push frequency: 20ms
    #
    #     Option:
    #     Level 25 data, push frequency: 20ms
    #     Level 100 data, push frequency: 100ms
    #
    #     Required args:
    #         symbol (string): Symbol name
    #         depth (int): Orderbook depth
    #         callback:
    #
    #     Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
    #     """
    #     topic = f"orderbook.{depth}.{symbol}"
    #     self.subscribe(topic, callback)
    #
    # def trade_stream(self, symbol: str, callback):
    #     """
    #     Subscribe to the recent trades stream.
    #     After subscription, you will be pushed trade messages in real-time.
    #
    #     Push frequency: real-time
    #
    #     Required args:
    #         symbol (string): Symbol name
    #
    #      Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/trade
    #     """
    #     topic = f"publicTrade.{symbol}"
    #     self.subscribe(topic, callback)
    #
    # def ticker_stream(self, symbol: str, callback):
    #     """Subscribe to the ticker stream.
    #
    #     Push frequency: 100ms
    #
    #     Required args:
    #         symbol (string): Symbol name
    #
    #      Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/ticker
    #     """
    #     topic = f"ticker.{symbol}"
    #     self.subscribe(topic, callback)
    #
    # def kline_stream(self, interval: int, symbol: str, callback):
    #     """Subscribe to the klines stream.
    #
    #     Push frequency: 1-60s
    #
    #     Required args:
    #         symbol (string): Symbol name
    #         interval (int): Kline interval
    #
    #      Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/kline
    #     """
    #     topic = f"kline.{interval}.{symbol}"
    #     self.subscribe(topic, callback)
    #
    # def liquidation_stream(self, symbol: str, callback):
    #     """Subscribe to the klines stream.
    #
    #     Push frequency: 1-60s
    #
    #     Required args:
    #         symbol (string): Symbol name
    #
    #      Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/kline
    #     """
    #     topic = f"liquidation.{symbol}"
    #     self.subscribe(topic, callback)
    #
    # def lt_kline_stream(self, interval: int, symbol: str, callback):
    #     """Subscribe to the leveraged token kline stream.
    #
    #     Push frequency: 1-60s
    #
    #     Required args:
    #         symbol (string): Symbol name
    #         interval (int): Leveraged token Kline stream interval
    #
    #      Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/etp-kline
    #     """
    #     topic = f"kline_lt.{interval}.{symbol}"
    #     self.subscribe(topic, callback)
    #
    # def lt_ticker_stream(self, symbol: str, callback):
    #     """Subscribe to the leveraged token ticker stream.
    #
    #     Push frequency: 300ms
    #
    #     Required args:
    #         symbol (string): Symbol name
    #
    #      Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/etp-ticker
    #     """
    #     topic = f"tickers_lt.{symbol}"
    #     self.subscribe(topic, callback)
    #
    # def lt_nav_stream(self, symbol: str, callback):
    #     """Subscribe to the leveraged token nav stream.
    #
    #     Push frequency: 300ms
    #
    #     Required args:
    #         symbol (string): Symbol name
    #
    #      Additional information:
    #         https://bybit-exchange.github.io/docs/v5/websocket/public/etp-nav
    #     """
    #     topic = f"lt.{symbol}"
    #     self.subscribe(topic, callback)
