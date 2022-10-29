from fastapi import FastAPI
from scraper import *
app = FastAPI()


@app.get("/")
def root():
    return ["a", "b"]


@app.get("/scrape{state}")
def scrapeAll(state: str):
    if fetch(state):
        return "success"
    else:
        return "failed"
