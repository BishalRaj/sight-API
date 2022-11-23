import logging
from fastapi import APIRouter
from pydantic import BaseModel
from controller.scraper.ups_us import fetch
from controller.scraper.multiplePage import getProductData, scrapeSingleProduct
from controller.dataHandler.etzy import saveItemTrackingData, saveItemData, getSingleDataFromDatabase, getAllDataByUser
from schemas.item import itemEntity, itemsEntity
from model.item import Item, TrackItem
from controller.auth import jwt_handler
scrapeRouter = APIRouter()

logger = logging.getLogger('ftpuploader')


class ItemURL(BaseModel):
    url: str


class SaveItem(BaseModel):
    token: str
    pid: str


@scrapeRouter.get('/scrape/ups/{state}')
def fetchALl(state: str):
    if fetch(state):
        return "success"
    else:
        return "failed"


@scrapeRouter.get('/scrape/etzy/{keyword}')
def fetchALl(keyword: str):
    if getProductData(keyword):
        return "success"
    else:
        return "failed"


@scrapeRouter.post('/scrape/etzy/single')
def fetchSingle(data: ItemURL):
    response = scrapeSingleProduct(data.url)
    if not response:
        return
    result = response[0]
    try:
        isAlreadySaved = getSingleDataFromDatabase(result['pid'])
        if not isAlreadySaved:
            res = saveItemData(result)
            result['id'] = str(res)
    except Exception as e:
        logger.error(e)
    return result


# @scrapeRouter.post('/scrape/etzy/single/data')
# def getSingleDatabase(data):
#     getSingleDataFromDatabase(data)


@scrapeRouter.post('/scrape/etzy/single/track')
def saveTracking(data: TrackItem):
    isValidUser = jwt_handler.decodeJWT(data.token)

    if isValidUser is None:
        return {"msj": "Session Expired"}

    if (isValidUser == {}):
        return {"msj": "Invalid User"}
    res = saveItemTrackingData(isValidUser['userID'], data.pid)
    return res


@scrapeRouter.get('/tracking/all/{token}')
def getTrackingByUser(token: str):
    isValidUser = jwt_handler.decodeJWT(token)

    if isValidUser is None:
        return {"msj": "Session Expired"}

    if (isValidUser == {}):
        return {"msj": "Invalid User"}
    res = getAllDataByUser(isValidUser['userID'])
    return res


@scrapeRouter.get('/scrape/amazon/all/{keyword}')
def fetchAll(keyword: str):
    if keyword[-1] == " ":
        keyword = keyword.rstrip(keyword[-1])
    return keyword
