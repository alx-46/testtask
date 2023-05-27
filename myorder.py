import random
import requests
from binance.client import Client


class Order:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = None

    # check access to API
    @staticmethod
    def check_api_access():
        try:
            requests.get("https://api.binance.com/api/v3/ping")
        except Exception:
            raise RuntimeError('Failed to connect to Binance.com')

    def create_orders(self, data):
        self.check_api_access()

        self.client = Client(self.api_key, self.api_secret)
        orders = []
        total_volume = data['volume']

        # checking incorrect input data
        required_fields = ['pair', 'side', 'volume', 'number', 'amountDif', 'priceMin', 'priceMax']
        if not all(field in data for field in required_fields) or any(data[field] <= 0 for field in
                                                                      required_fields[2:]):
            raise ValueError("Missing required fields or invalid values in data")

        # get information about pair
        exchange_info = self.client.get_exchange_info()
        symbol_info = next((symbol for symbol in exchange_info['symbols'] if symbol['symbol'] == data['pair']),
                           None)
        if not symbol_info:
            raise ValueError(f"Invalid pair: {data['pair']}")

        for i in range(data['number']):
            # !!! with a small data['volume'],  summa of order volume is sometimes less than data['volume']
            order_volume = round(min(total_volume, data['volume'] / data['number'] + random.uniform(-data['amountDif'],
                                     data['amountDif'])), 4)
            order_price = random.uniform(data['priceMin'], data['priceMax'])

            try:
                order = self.client.create_order(
                    symbol=data['pair'],
                    side=data['side'],
                    type=Client.ORDER_TYPE_LIMIT,
                    timeInForce=Client.TIME_IN_FORCE_GTC,
                    quantity=order_volume,
                    price=format(order_price, '.2f')
                )
                orders.append(order)
                total_volume -= order_volume
            except Exception as e:
                raise RuntimeError("Failed to create order: " + str(e))

        return orders

    def check_orders(self, pair):
        self.check_api_access()

        self.client = Client(self.api_key, self.api_secret)
        try:
            active_orders = self.client.get_open_orders(symbol=pair)
        except Exception as e:
            raise RuntimeError("Failed to check orders: " + str(e))

        return active_orders
