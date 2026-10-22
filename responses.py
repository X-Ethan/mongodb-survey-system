from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from bson import ObjectId
from database import surveys_col, questions_col, responses_col
from auth import get_current_user
from models import ResponseSubmit

router = APIRouter()

@router.get("/surveys/share/{share_code}")
def get_survey_by_share(share_code: str):
    survey = surveys_col.find_one({"share_code": share_code, "status": "published"})
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found or not published")
    survey["_id"] = str(survey["_id"])
    questions = list(questions_col.find({"survey_id": survey["_id"]}).sort("order", 1))
    for q in questions:
        q["_id"] = str(q["_id"])
    survey["questions"] = questions
    return survey

@router.post("/surveys/{survey_id}/responses")
def submit_response(survey_id: str, body: ResponseSubmit, current_user: dict = Depends(get_current_user)):
    survey = surveys_col.find_one({"_id": ObjectId(survey_id), "status": "published"})
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not available")
    doc = {
        "survey_id": survey_id,
        "user_id": str(current_user["_id"]),
        "answers": [a.dict() for a in body.answers],
        "submitted_at": datetime.utcnow()
    }
    result = responses_col.insert_one(doc)
    return {"response_id": str(result.inserted_id)}

@router.get("/surveys/{survey_id}/stats")
def get_stats(survey_id: str, current_user: dict = Depends(get_current_user)):
    survey = surveys_col.find_one({"_id": ObjectId(survey_id), "creator_id": str(current_user["_id"])})
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    questions = list(questions_col.find({"survey_id": survey_id}))
    responses = list(responses_col.find({"survey_id": survey_id}))
    stats = []
    for q in questions:
        qid = str(q["_id"])
        item = {"question_id": qid, "title": q["title"], "type": q["type"]}
        if q["type"] == "single":
            counts = {opt: 0 for opt in q["options"]}
            for r in responses:
                for a in r["answers"]:
                    if a.get("question_id") == qid and a.get("value") in counts:
                        counts[a["value"]] += 1
            item["counts"] = counts
            item["total"] = sum(counts.values())
        elif q["type"] == "multiple":
            counts = {opt: 0 for opt in q["options"]}
            for r in responses:
                for a in r["answers"]:
                    if a.get("question_id") == qid:
                        for v in a.get("value", []):
                            if v in counts:
                                counts[v] += 1
            item["counts"] = counts
        elif q["type"] == "number":
            nums = []
            for r in responses:
                for a in r["answers"]:
                    if a.get("question_id") == qid and isinstance(a.get("value"), (int, float)):
                        nums.append(a["value"])
            item["values"] = nums
            item["avg"] = sum(nums) / len(nums) if nums else 0
        else:
            texts = []
            for r in responses:
                for a in r["answers"]:
                    if a.get("question_id") == qid:
                        texts.append(a.get("value"))
            item["answers"] = texts
        stats.append(item)
    return {"survey_id": survey_id, "response_count": len(responses), "stats": stats}
