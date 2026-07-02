from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.users import User
from schemas.users import UserCreate, UserResponse, Login_User
from utils.security import hash_password, verify_password
from utils.token import create_access_token
from schemas.token import Token
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse )
def register(user: UserCreate, db: Session = Depends(get_db)):
   
    existing_user = db.query(User).filter((User.name == user.name) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Name or email already registered")

  
    try:
        hashed_password = hash_password(user.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

   
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role  
    )

  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=Token)
def login(user: Login_User, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user :
        raise HTTPException(status_code=404, detail="User not Found")
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token=create_access_token(data={"sub":str(existing_user.id), "role":existing_user.role})
    return {"token": access_token, "token_type": "Bearer"}
