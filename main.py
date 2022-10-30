from fastapi import FastAPI
from config.scraper import *
from routes.user import user
app = FastAPI()

app.include_router(user)


@app.get("/scrape{state}")
def scrapeAll(state: str):
    if fetch(state):
        return "success"
    else:
        return "failed"
