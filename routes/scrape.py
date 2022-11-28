import logging
import time
from fastapi import APIRouter
from pydantic import BaseModel
from controller.scraper.ups_us import fetch
from controller.scraper.etzy import getProductData, scrapeSingleProduct, automateTracking
from controller.dataHandler.etzy import saveItemTrackingData, saveItemData, getSingleDataFromDatabase, getAllDataByUser, saveItemMicroData
from model.item import TrackItem
from controller.auth import jwt_handler
from fastapi.responses import FileResponse

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
    # return
    return FileResponse(getProductData(keyword))
    # return getProductData(keyword)


@scrapeRouter.post('/scrape/etzy/single')
async def fetchSingle(data: ItemURL):
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

    res = saveItemMicroData({"pid": result['pid'], "price": result['price'], "date": time.time(),
                             "sales": result['sales'], "rating": result['rating'], "review": result['review']})

    return result


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


@scrapeRouter.get('/scrape/automate')
def automate():
    return automateTracking()
