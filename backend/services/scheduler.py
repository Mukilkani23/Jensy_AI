import asyncio
from db.connection import get_database
from services.scraper import scrape_college_curriculum
from datetime import datetime

class MockScheduler:
    def add_job(self, *args, **kwargs): pass
    def start(self): pass
    def shutdown(self): pass

scheduler = MockScheduler()


async def scrape_job():
    db = get_database()
    print("Running automated syllabus scraper...")
    # Get all unique college urls from curriculum
    urls = await db.curriculum.distinct("college_url")
    for url in urls:
        if not url:
            continue
        try:
            new_data = await scrape_college_curriculum(url)
            # Find existing
            existing = await db.scraped_syllabus.find_one({"source_url": url})
            if existing:
                # Simple diff check on semesters keys
                if set(existing.get("semesters", {}).keys()) != set(new_data.get("semesters", {}).keys()):
                    print(f"Syllabus changed for {url}")
                    # Notify users
                    users = await db.students.find({"college_url": url}).to_list(length=1000)
                    for u in users:
                        await db.notifications.insert_one({
                            "student_id": str(u["_id"]),
                            "message": "Syllabus has been updated for your college.",
                            "read": False,
                            "created_at": datetime.utcnow()
                        })
            
            # Update storage
            await db.scraped_syllabus.update_one(
                {"source_url": url},
                {"$set": new_data},
                upsert=True
            )
        except Exception as e:
            print(f"Scraper job failed for {url}: {e}")

def start_scheduler():
    scheduler.add_job(scrape_job, 'interval', weeks=1)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()
