def itemEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "pid": item["pid"],
        "name": item["name"],
        "price": item["price"],
        "rating": item["rating"],
        "sales": item["sales"],
        "review": item["review"],
        "img": item["img"],
        "url": item["url"]
    }


def itemsEntity(entity) -> list:
    return [itemEntity(item) for item in entity]
