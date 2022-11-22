from schemas.item import itemEntity, itemsEntity
import logging
from config.db import conn
from model.item import Item, TrackItem
from schemas.item import itemsEntity
from bson import json_util
import json
logger = logging.getLogger('ftpuploader')

itemDB = conn.sight.item
trackingDB = conn.sight.tracker


def saveItemData(data):
    try:
        res = itemDB.insert_one(dict(data)).inserted_id
        return res
    except Exception as e:
        logger.error(e)


def saveItemTrackingData(data: TrackItem):
    return data
