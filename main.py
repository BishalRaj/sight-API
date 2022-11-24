from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.scraper.ups_us import fetch
from routes.user import userRouter
from routes.scrape import scrapeRouter
from fastapi_utils.tasks import repeat_every
from controller.scraper.etzy import automateTracking

app = FastAPI()

# origins = ['https://localhost:3000','http://localhost:3000', 'http://127.0.0.1:3000']
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(userRouter)
app.include_router(scrapeRouter)


@app.on_event("startup")
@repeat_every(seconds=60)  # 6 Hours
def automate():
    try:
        automateTracking()
    except Exception as e:
        print(e)
