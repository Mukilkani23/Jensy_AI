import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add backend dir to path for imports
sys.path.insert(0, os.path.dirname(__file__))

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from db.connection import connect_to_mongo, close_mongo_connection, get_database
from routes.auth import router as auth_router
from routes.student import router as student_router
from routes.curriculum import router as curriculum_router
from routes.resources import router as resources_router
from routes.progress import router as progress_router
from routes.ai import router as ai_router
from routes.planner import router as planner_router
from routes.admin import router as admin_router
from routes.attendance import router as attendance_router
from routes.career import router as career_router
from routes.analytics import router as analytics_router
from services.seed import seed_database


from services.scheduler import start_scheduler, stop_scheduler







@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    db = get_database()
    await seed_database(db)
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()
    await close_mongo_connection()



app = FastAPI(
    title="GENZ API",
    description="Academic Companion Platform for Bachelor's Degree Students",
    version="1.0.0",
    lifespan=lifespan,
)

# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(curriculum_router)
app.include_router(resources_router)
app.include_router(progress_router)
app.include_router(ai_router)
app.include_router(planner_router)
app.include_router(admin_router)
app.include_router(attendance_router)
app.include_router(career_router)
app.include_router(analytics_router)






@app.get("/")
async def root():
    return {
        "app": "GENZ",
        "version": "1.0.0",
        "description": "Academic Companion Platform for Bachelor's Degree Students",
        "docs": "/docs"
    }


@app.post("/admin/curriculum/add")
async def admin_add_curriculum(curriculum_data: dict):
    """Admin endpoint to add new regulation curriculum."""
    db = get_database()
    result = await db.curriculum.insert_one(curriculum_data)
    return {"message": "Curriculum added", "id": str(result.inserted_id)}
