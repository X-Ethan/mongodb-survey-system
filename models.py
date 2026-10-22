from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SurveyCreate(BaseModel):
    title: str
    description: str = ""
    allow_anonymous: bool = False
    deadline: Optional[str] = None

class QuestionCreate(BaseModel):
    type: str
    title: str
    required: bool = True
    options: List[str] = []
    validation: Dict = {}

class AnswerItem(BaseModel):
    question_id: str
    value: Any

class ResponseSubmit(BaseModel):
    answers: List[AnswerItem]
