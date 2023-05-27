from myorder import Order
import time

# example of using and checking the creation and placement of orders
api_key = ''
api_secret = ''

client = Order(api_key, api_secret)

data = {
    'pair': 'ETHUSDT',
    'volume': 0.05,
    'number': 5,
    'amountDif': 0.001,
    'side': "SELL",
    'priceMin': 2050,
    'priceMax': 2150
}

try:
    placed_orders = client.create_orders(data)
    time.sleep(1)
    active_orders = client.check_orders(data['pair'])
    ids_of_active_orders = {order['orderId'] for order in active_orders}

    for order in placed_orders:
        result = 'created and posted' if order['orderId'] in ids_of_active_orders else 'created but not posted'
        price = round(float(order['price']), 2)
        quantity = round(float(order['origQty']), 4)
        print(f"Order Id: {order['orderId']} {result}: {order['symbol']}, {order['side']}, {price}, {quantity}")

except Exception as e:
    print(e)

