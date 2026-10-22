from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["survey_system"]

users_col = db["users"]
surveys_col = db["surveys"]
questions_col = db["questions"]
responses_col = db["responses"]
