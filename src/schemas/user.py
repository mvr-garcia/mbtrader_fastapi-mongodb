def user_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "balance_brl": item["balance_brl"],
        "balance_btc": item["balance_btc"],
        "balance_eth": item["balance_eth"],
        "created": item["created"]
    }


def users_entity(entity) -> list:
    return [user_entity(item) for item in entity]
