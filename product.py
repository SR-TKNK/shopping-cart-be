def productEntityAdd(item) -> dict:
    return {
        "message": "add",
        "code": str(item["code"]),
        "name": str(item["name"]),
        "price": int(item["price"]),
        "weight": int(item["weight"])
    }


def productEntityDelete(item) -> dict:
    return {
        "message": "delete",
        "code": str(item["code"]),
        "name": str(item["name"]),
        "price": int(item["price"]),
        "weight": int(item["weight"])
    }
