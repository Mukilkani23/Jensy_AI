from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from models.student import OnboardingSetup
from models.curriculum import CurriculumCreate, CurriculumResponse, Subject
from utils.auth_utils import get_current_user
from db.connection import get_database
from services.scraper import scrape_college_curriculum

router = APIRouter(tags=["Curriculum & Onboarding"])


@router.post("/onboarding/setup")
async def onboarding_setup(data: OnboardingSetup, user: dict = Depends(get_current_user)):
    db = get_database()
    student_id = user["user_id"]

    update_data = {
        "degree": data.degree,
        "branch": data.branch,
        "college_type": data.college_type,
        "college_url": data.college_url,
        "regulation": data.regulation,
        "preference": data.preference,
        "semester_current": data.semester_current,
    }

    await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": update_data}
    )

    return {"message": "Onboarding data saved successfully"}


@router.post("/onboarding/scrape")
async def onboarding_scrape(college_url: str, user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        curriculum_data = await scrape_college_curriculum(college_url)

        college_doc = {
            "name": curriculum_data.get("college_name", "Unknown"),
            "url": college_url,
            "is_autonomous": True,
            "scraped_curriculum": curriculum_data,
        }
        existing = await db.colleges.find_one({"url": college_url})
        if existing:
            await db.colleges.update_one({"url": college_url}, {"$set": college_doc})
        else:
            await db.colleges.insert_one(college_doc)

        return {"message": "Curriculum scraped and saved", "data": curriculum_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.get("/curriculum/{student_id}")
async def get_curriculum(student_id: str, user: dict = Depends(get_current_user)):
    db = get_database()
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    degree = student.get("degree", "")
    regulation = student.get("regulation", "")
    branch = student.get("branch", "")

    query = {"degree": degree}
    if regulation:
        query["regulation"] = regulation

    curricula = await db.curriculum.find(query).sort("semester", 1).to_list(length=100)

    result = []
    for c in curricula:
        result.append({
            "id": str(c["_id"]),
            "degree": c["degree"],
            "regulation": c.get("regulation", ""),
            "semester": c["semester"],
            "subjects": c.get("subjects", [])
        })

    return {"curriculum": result, "degree": degree, "branch": branch, "regulation": regulation}
