from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from bson import ObjectId
from database import surveys_col, questions_col
from auth import get_current_user
from models import SurveyCreate, QuestionCreate
import secrets

router = APIRouter()

@router.post("/surveys")
def create_survey(survey: SurveyCreate, current_user: dict = Depends(get_current_user)):
    share_code = secrets.token_urlsafe(8)
    doc = {
        "creator_id": str(current_user["_id"]),
        "title": survey.title,
        "description": survey.description,
        "allow_anonymous": survey.allow_anonymous,
        "status": "draft",
        "deadline": survey.deadline,
        "share_code": share_code,
        "created_at": datetime.utcnow()
    }
    result = surveys_col.insert_one(doc)
    return {"survey_id": str(result.inserted_id), "share_code": share_code}

@router.get("/surveys")
def list_my_surveys(current_user: dict = Depends(get_current_user)):
    surveys = list(surveys_col.find({"creator_id": str(current_user["_id"])}))
    for s in surveys:
        s["_id"] = str(s["_id"])
    return surveys

@router.post("/surveys/{survey_id}/publish")
def publish_survey(survey_id: str, current_user: dict = Depends(get_current_user)):
    result = surveys_col.update_one(
        {"_id": ObjectId(survey_id), "creator_id": str(current_user["_id"])},
        {"$set": {"status": "published"}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Published"}

@router.post("/surveys/{survey_id}/questions")
def add_question(survey_id: str, question: QuestionCreate, current_user: dict = Depends(get_current_user)):
    survey = surveys_col.find_one({"_id": ObjectId(survey_id), "creator_id": str(current_user["_id"])})
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    order = questions_col.count_documents({"survey_id": survey_id}) + 1
    doc = {
        "survey_id": survey_id,
        "order": order,
        "type": question.type,
        "title": question.title,
        "required": question.required,
        "options": question.options,
        "validation": question.validation,
        "jump_rules": []
    }
    result = questions_col.insert_one(doc)
    return {"question_id": str(result.inserted_id), "order": order}
