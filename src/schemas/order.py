def order_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "fiat": item["fiat"],
        "symbol": item["symbol"],
        "pair": item["pair"],
        "order_type": item["order_type"],
        "quantity": item["quantity"],
        "fee": item["fee"],
        "net_quantity": item["net_quantity"],
        "created": item["created"]
    }


def orders_entity(entity) -> list:
    return [order_entity(item) for item in entity]
