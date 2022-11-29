from pymongo import MongoClient
from decouple import config
conn = MongoClient(config("db"))
