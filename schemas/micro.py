import time


def microEntity(item) -> dict:

    return {
        "id": str(item["_id"]),
        "pid": item["pid"],
        "date": str(time.strftime('%Y-%m-%d', time.localtime(item["date"]))),
        "price": item["price"],
        "rating": item["rating"],
        "sales": item["sales"],
        "review": item["review"],
    }


def microsEntity(entity) -> list:
    return [microEntity(item) for item in entity]
