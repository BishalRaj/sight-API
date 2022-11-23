def trackingEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "pid": item["pid"],
        "username": item["username"],
    }


def trackingsEntity(entity) -> list:
    return [trackingEntity(item) for item in entity]
