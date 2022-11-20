from fastapi import APIRouter
from pydantic import BaseModel
from controller.scraper.ups_us import fetch
from controller.scraper.multiplePage import getProductData, getSingleProduct
scrapeRouter = APIRouter()


class Item(BaseModel):
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
def fetchSingle(data: Item):
    # print(url)
    response = getSingleProduct(data.url)
    if response:
        response = response[0]
    return response


@scrapeRouter.post('/scrape/etzy/single/save')
def saveSingle(data: SaveItem):
    print(data.token)


@scrapeRouter.get('/scrape/amazon/all/{keyword}')
def fetchAll(keyword: str):
    if keyword[-1] == " ":
        keyword = keyword.rstrip(keyword[-1])
    return keyword
