from schemas.tracking import trackingsEntity
import logging
from config.db import conn
logger = logging.getLogger('ftpuploader')


itemDB = conn.sight.item
trackingDB = conn.sight.tracker
microTrackingDB = conn.sight.micro


def saveItemData(data):
    try:
        res = itemDB.insert_one(dict(data)).inserted_id
        return res
    except Exception as e:
        logger.error(e)


def saveItemMicroData(data):
    try:
        res = microTrackingDB.insert_one(dict(data)).inserted_id
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


def getUserFromTrackingDB(pid: str):
    res = trackingsEntity(trackingDB.find({"pid": pid}))
    users = []
    for user in res:
        users.append(user['username'])
    return users


def updateProductData(data):
    itemDB.find_one_and_update({'pid': data["pid"]}, {"$set": data})
