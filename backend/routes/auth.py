from fastapi import APIRouter, HTTPException, status, Depends
from models.student import StudentCreate, StudentLogin, StudentInDB
from utils.auth_utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.connection import get_database
from datetime import datetime
from bson import ObjectId


router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()



@router.post("/register")
async def register(student: StudentCreate):
    db = get_database()
    existing = await db.students.find_one({"email": student.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    student_doc = StudentInDB(
        name=student.name,
        email=student.email,
        password_hash=hash_password(student.password),
        role="student",
        created_at=datetime.utcnow()
    )
    result = await db.students.insert_one(student_doc.model_dump())
    
    token_data = {"sub": str(result.inserted_id), "email": student.email, "role": "student"}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "message": "Registration successful",
        "token": access_token,
        "refresh_token": refresh_token,
        "student_id": str(result.inserted_id)
    }



@router.post("/login")
async def login(credentials: StudentLogin):
    db = get_database()
    student = await db.students.find_one({"email": credentials.email})
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(credentials.password, student["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token_data = {"sub": str(student["_id"]), "email": student["email"], "role": student.get("role", "student")}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "message": "Login successful",
        "token": access_token,
        "refresh_token": refresh_token,
        "student_id": str(student["_id"])
    }


@router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    db = get_database()
    student = await db.students.find_one({"_id": ObjectId(payload.get("sub"))})
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    token_data = {
        "sub": str(student["_id"]), 
        "email": student.get("email"), 
        "role": student.get("role", "student")
    }

    
    new_access_token = create_access_token(token_data)
    
    return {
        "token": new_access_token
    }
