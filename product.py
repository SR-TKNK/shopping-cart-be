def productEntityAdd(item) -> dict:
    return {
        "code": str(item["code"]),
        "name": str(item["name"]),
        "price": int(item["price"]),
        "weight": int(item["weight"])
    }

def productEntityDelete(item) -> dict:
    return {
        "id": str(item["_id"])
    }
