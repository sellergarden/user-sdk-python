class ExecEnvironment:
    def __init__(self, **kwargs):
        self.digikala_seller_api_key = kwargs.get("digikala_seller_api_key")
        self.kv_store_url = kwargs.get("kv_store_url")

    def __repr__(self):
        return (
            "ExecEnvironment("
            + f"\tdigikala_seller_api_key={self.digikala_seller_api_key},"
            + f"\tkv_store_url={self.kv_store_url}"
            + ")"
        )
