import datetime

import pandas as pd
from lumibot.backtesting import BacktestingBroker, PandasDataBacktesting
from lumibot.entities import Asset, Data
from lumibot.strategies import Strategy
from lumibot.traders import Trader

import signals

BTC_ASSET = Asset(symbol="SOL", asset_type=Asset.AssetType.CRYPTO)
USDT_ASSET = Asset(symbol="USDT", asset_type=Asset.AssetType.CRYPTO)


# A simple strategy that buys SPY on the first day
class MyStrategy(Strategy):
#    def initialize(self):
#        self.minutes_before_closing = 0
#        self.minutes_before_opening = 0

    def position_sizing(self):
        current_price = self.get_last_price(BTC_ASSET)
        current_cash = self.get_cash()
        if current_cash < 0.0:
            raise ValueError("NO CASH")
        quantity = current_cash // current_price
        return quantity

    def count_open_orders(self, orders):
        for order in orders:
            self.log_message(f"orders status: {order.status}", color='red')
        open_orders = [order for order in orders if order.status == "new"]
        return len(open_orders)

    def on_trading_iteration(self):
        print(f"Timezone of the strategy: {self.timezone}")
        stop_quote = 0.01
        limit_quote = 0.015
        cash = 0.05
        if self.first_iteration:
            self.set_parameters({"name":"Harami",
                             "asset" : "SOLUSDT",
                             "stop": stop_quote, "limit": limit_quote,
                             "cash":cash,
                             "rounding": False,
                             "one_order": True})

            quantity_to_buy = self.position_sizing()
            order = self.create_order(asset=BTC_ASSET, quantity=quantity_to_buy, side="buy", quote=USDT_ASSET)
            self.submit_order(order)
            print("order submitted")

#        parameters = self.get_parameters()
#        print(f"parameters: {parameters}")
#        all_orders = self.get_orders()
#        open_orders_count = self.count_open_orders(all_orders)
#        self.log_message(f"Open orders count: {open_orders_count}")
#        if open_orders_count <= 1:
#            self.cancel_open_orders()
#            las_prices_bars = self.get_historical_prices(BTC_ASSET, 4, timestep='minute')
#            if las_prices_bars and len(las_prices_bars.df) >= 4:
#                df_last_prices = las_prices_bars.df
#                first = df_last_prices.iloc[0]
#                print(first)
#                second = df_last_prices.iloc[1]
#                print(second)
#                third = df_last_prices.iloc[2]
#                print(third)
#                current_price = self.get_last_price(BTC_ASSET)
#                is_doppelganger = signals.is_harami(
#                    first=first,
#                    second=second,
#                )
#                if is_doppelganger:
#                    quantity = self.position_sizing()
#                    order = self.create_order(asset=BTC_ASSET, quantity=quantity, side="buy")
#                    self.submit_order(order)
#                    #cash reward
#                    order_reward = self.create_order(asset=BTC_ASSET,
#                                                     quantity=quantity,
#                                                     side="sell",
#                                                     limit_price=current_price + current_price*cash)
#                    self.submit_order(order_reward)
#                    #stop loss
#                    order_stop_loss = self.create_order(asset=BTC_ASSET,
#                                                        quantity=quantity,
#                                                        side="sell",
#                                                        stop_price=current_price - current_price*stop_quote,
#                                                        limit_price=current_price - current_price*limit_quote
#                                                        )
#                    self.submit_order(order_stop_loss)
#                    print("order submitted")
#        current_cash = self.get_cash()
#        print(f"Current cash: {current_cash}")
#        current_portfolio_value = self.get_portfolio_value()
#        print(f"Current portfolio value: {current_portfolio_value}")
#        if current_cash < 0:
#            self.log_message(f"current cash below zero {current_cash}", color="red")
#



# Read the data from the CSV file (in this example you must have a file named "AAPL.csv"
# in a folder named "data" in the same directory as this script)
#df = pd.read_csv("./datasets/BTCUSDT_1m_202201_202303.csv")
df = pd.read_csv("./datasets/BTCUSDT_1m_202303_202403.csv")
df = pd.read_csv("./datasets/SOLUSDT_1m_2023_01_01_2024_04_01.csv")

pandas_data = {}
pandas_data[BTC_ASSET] = Data(BTC_ASSET, df,
                              timestep="minute",
                              quote=USDT_ASSET
                            )
# Pick the date range you want to backtest
backtesting_start = pandas_data[BTC_ASSET].datetime_start
print(f"this is backtesting_start: {backtesting_start}")
backtesting_end = pandas_data[BTC_ASSET].datetime_end
print(f"this is backtesting end: {backtesting_end}")

# Run the backtesting
trader = Trader(backtest=True, debug=True)
data_source = PandasDataBacktesting(
    pandas_data=pandas_data,
    datetime_start=backtesting_start,
    datetime_end=backtesting_end,
)
config = {"timezone": "Europe/London"}
broker = BacktestingBroker(data_source, config=config)
print(f" market close !!!!!!!{broker.market_close_time()}")
strat = MyStrategy(
    broker=broker,
    budget=1000000,
    quote_asset=USDT_ASSET,
)
trader.add_strategy(strat)
trader.run_all()
