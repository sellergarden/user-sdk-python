import json
import os
from enum import Enum

from sellergarden_sdk import ExecEnvironment


class Injectable:
    """
    Base class for any injectable. Any service or dependency
    that needs to be injected into the function should extend this class.
    """

    pass


class BotEventType(Enum):
    GOLD_PRICE = "gold_price"
    DOLLAR_PRICE = "dollar_price"
    # Add other event types as needed
    STOCK_MARKET = "stock_market"
    WEATHER_UPDATE = "weather_update"
    NEWS_UPDATE = "news_update"


class DigikalaSellerAPI(Injectable):

    def __init__(self, environment: ExecEnvironment):
        self.digikala_seller_api_key = environment.digikala_seller_api_key

    def GetShouldPackageVariants(self, from_date, to_date):
        print(f"Fetching variants from {from_date} to {to_date}")
        return [
            {"id": 1, "name": "Variant 1"},
            {"id": 2, "name": "Variant 2"},
        ]  # Mocked data

    def GetWarehouseCapacity(self, warehouse_id):
        print(f"Fetching capacity for warehouse #{warehouse_id}")
        return [
            {"id": 101, "from": "09:00", "to": "17:00"},
            {"id": 102, "from": "17:00", "to": "23:00"},
        ]

    def CreatePackage(self, variants, warehouse_id, capacity_id):
        print(
            f"Creating package for variants {variants} in warehouse {warehouse_id} with capacity {capacity_id}"
        )
        return {"success": True}

    def GetOrders(self, from_date, to_date):
        print(f"Fetching orders from {from_date} to {to_date}")
        return [
            {"id": 1, "name": "Order 1", "products": [1, 2], "total_price": 100},
            {"id": 2, "name": "Order 2", "products": [2], "total_price": 50},
        ]

    def GetProducts(self, from_date, to_date):
        print(f"Fetching products from {from_date} to {to_date}")
        return [
            {"id": 1, "name": "Product 1"},
            {"id": 2, "name": "Product 2"},
        ]


class AppKVStore(Injectable):
    """ """

    def __init__(self, environment: ExecEnvironment):
        self.data = {}
        self.kv_store_url = environment.kv_store_url
        # load data from json file
        if os.path.exists(self.kv_store_url):
            with open(self.kv_store_url) as f:
                self.data = json.load(f)
        else:
            # create empty file
            with open(self.kv_store_url, "w") as f:
                json.dump({}, f)

    def getData(self, key):
        return self.data.get(key)

    def setData(self, key, value):
        self.data[key] = value
        print(f"Saved {value} under {key}")
        # save data to json file
        with open("db_url", "w") as f:
            json.dump(self.data, f)


helper_classes = [DigikalaSellerAPI, AppKVStore]
