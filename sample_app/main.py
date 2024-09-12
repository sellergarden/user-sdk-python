from sellergarden_sdk.decorators import Api
from sellergarden_sdk.helpers import DigikalaSellerAPI


@Api("/average-order-price")
def my_aggregator(sellerApi: DigikalaSellerAPI):
    orders = sellerApi.GetOrders()

    # calculate average price of orders
    total_price = 0
    for order in orders:
        total_price += order["total_price"]

    average_price = total_price / len(orders)

    # return api response
    return {"average_price": average_price}, 200
