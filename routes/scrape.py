from fastapi import APIRouter

from controller.scraper.ups_us import fetch
scrapeRouter = APIRouter()


@scrapeRouter.get('/scrape/{state}')
async def fetchALl(state: str):
    if fetch(state):
        return "success"
    else:
        return "failed"
