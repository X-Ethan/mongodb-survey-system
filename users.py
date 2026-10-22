from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from models import UserRegister, UserLogin, Token
from database import users_col
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):
    if users_col.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    users_col.insert_one({
        "username": user.username,
        "password_hash": hash_password(user.password),
        "created_at": datetime.utcnow()
    })
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    db_user = users_col.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "created_at": current_user["created_at"]}
