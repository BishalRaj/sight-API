from schemas.tracking import trackingsEntity
import logging
from config.db import conn
from schemas.item import itemsEntity

logger = logging.getLogger('ftpuploader')


itemDB = conn.sight.item
trackingDB = conn.sight.tracker


def saveItemData(data):
    try:
        res = itemDB.insert_one(dict(data)).inserted_id
        return res
    except Exception as e:
        logger.error(e)


def saveItemTrackingData(un, pid):
    try:
        res = trackingDB.insert_one(
            dict({'username': un, 'pid': pid})).inserted_id
        return str(res)

    except Exception as e:
        logger.error(e)


def getSingleDataFromDatabase(data):
    return itemDB.find_one({"pid": data})


def getAllDataByUser(username: str):
    data = []
    res = trackingsEntity(trackingDB.find({"username": username}))
    for doc in res:
        itemData = itemDB.find_one({"pid": doc["pid"]})
        data.append({
            "pid": itemData["pid"],
            "name": itemData["name"],
            "price": itemData["price"],
            "rating": itemData["rating"],
            "sales": itemData["sales"],
            "review": itemData["review"],
            "img": itemData["img"],
            "url": itemData["url"]
        })
    return data
