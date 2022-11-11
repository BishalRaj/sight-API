from fastapi import APIRouter

from controller.scraper.ups_us import fetch
from controller.scraper.multiplePage import getAllData

scrapeRouter = APIRouter()


@scrapeRouter.get('/scrape/ups/{state}')
async def fetchALl(state: str):
    if fetch(state):
        return "success"
    else:
        return "failed"


@scrapeRouter.get('/scrape/amazon/{keyword}')
async def fetchALl(keyword: str):
    if getAllData(keyword):
        return "success"
    else:
        return "failed"


@scrapeRouter.get('/scrape/amazon/all/{keyword}')
async def fetchAll(keyword: str):
    if keyword[-1] == " ":
        keyword = keyword.rstrip(keyword[-1])
    return keyword
