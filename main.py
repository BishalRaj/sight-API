from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.scraper.ups_us import fetch
from routes.user import userRouter
from routes.scrape import scrapeRouter
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
