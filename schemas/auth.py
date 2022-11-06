def authEntity(item) -> dict:
    return {

        "email": item["email"],
        "password": item["password"]
    }


def authenticationEntity(entity) -> list:
    return [authEntity(item) for item in entity]
