from fastapi import FastAPI
from database import db
from routers.users import router as users_router
from routers.surveys import router as surveys_router
from routers.responses import router as responses_router

app = FastAPI()
app.include_router(users_router)
app.include_router(surveys_router)
app.include_router(responses_router)

@app.get("/")
def root():
    return {"message": "Survey system running", "db": db.name}
