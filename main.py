from fastapi import FastAPI
app = FastAPI()


@app.get("/")
def root():
    return {"msg": "Hello world"}


@app.get("/home")
def home():
    return {"msg": "Home"}
