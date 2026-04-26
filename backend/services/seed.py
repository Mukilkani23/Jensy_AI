"""
Database seeder for GENZ — Seeds curriculum data for:
- B.E CSE (Reg 2021, Reg 2025)
- B.E ECE (Reg 2021, Reg 2025)
- B.E Mech (Reg 2021, Reg 2025)
- BSc CS (Reg 2021)
- BCom (Reg 2021)
"""


def get_seed_data():
    return [
        # ═══════════════════════════════════════
        # B.E CSE — Regulation 2021
        # ═══════════════════════════════════════
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 1, "subjects": [
            {"code": "MA3151", "name": "Matrices and Calculus", "type": "theory", "credits": 4},
            {"code": "PH3151", "name": "Engineering Physics", "type": "theory", "credits": 3},
            {"code": "CY3151", "name": "Engineering Chemistry", "type": "theory", "credits": 3},
            {"code": "GE3151", "name": "Problem Solving and Python Programming", "type": "theory", "credits": 3},
            {"code": "GE3152", "name": "Heritage of Tamils", "type": "theory", "credits": 1},
            {"code": "GE3171", "name": "Problem Solving and Python Programming Lab", "type": "lab", "credits": 2},
            {"code": "BS3171", "name": "Physics and Chemistry Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 2, "subjects": [
            {"code": "MA3251", "name": "Statistics and Numerical Methods", "type": "theory", "credits": 4},
            {"code": "BE3251", "name": "Basic Electrical and Electronics Engineering", "type": "theory", "credits": 3},
            {"code": "GE3251", "name": "Engineering Graphics", "type": "theory", "credits": 4},
            {"code": "CS3251", "name": "Programming in C", "type": "theory", "credits": 3},
            {"code": "GE3252", "name": "Tamils and Technology", "type": "theory", "credits": 1},
            {"code": "CS3271", "name": "Programming in C Lab", "type": "lab", "credits": 2},
            {"code": "GE3271", "name": "Engineering Practices Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 3, "subjects": [
            {"code": "MA3351", "name": "Discrete Mathematics", "type": "theory", "credits": 4},
            {"code": "CS3351", "name": "Digital Principles and Computer Organization", "type": "theory", "credits": 4},
            {"code": "CS3352", "name": "Foundations of Data Science", "type": "theory", "credits": 3},
            {"code": "CS3301", "name": "Data Structures", "type": "theory", "credits": 3},
            {"code": "CS3391", "name": "Object Oriented Programming", "type": "theory", "credits": 3},
            {"code": "CS3311", "name": "Data Structures Lab", "type": "lab", "credits": 2},
            {"code": "CS3381", "name": "Object Oriented Programming Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 4, "subjects": [
            {"code": "CS3452", "name": "Theory of Computation", "type": "theory", "credits": 3},
            {"code": "CS3491", "name": "Artificial Intelligence and Machine Learning", "type": "theory", "credits": 4},
            {"code": "CS3492", "name": "Database Management Systems", "type": "theory", "credits": 3},
            {"code": "CS3401", "name": "Algorithms", "type": "theory", "credits": 4},
            {"code": "CS3451", "name": "Introduction to Operating Systems", "type": "theory", "credits": 3},
            {"code": "CS3461", "name": "Operating Systems Lab", "type": "lab", "credits": 2},
            {"code": "CS3481", "name": "Database Management Systems Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 5, "subjects": [
            {"code": "CS3591", "name": "Computer Networks", "type": "theory", "credits": 3},
            {"code": "CS3501", "name": "Compiler Design", "type": "theory", "credits": 4},
            {"code": "CB3491", "name": "Cryptography and Cyber Security", "type": "theory", "credits": 3},
            {"code": "CS3551", "name": "Distributed Computing", "type": "theory", "credits": 3},
            {"code": "CCS356", "name": "Object Oriented Software Engineering", "type": "theory", "credits": 3},
            {"code": "CS3511", "name": "Compiler Design Lab", "type": "lab", "credits": 2},
            {"code": "CS3581", "name": "Networks Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 6, "subjects": [
            {"code": "CCS354", "name": "Machine Learning", "type": "theory", "credits": 3},
            {"code": "CS3691", "name": "Embedded Systems and IoT", "type": "theory", "credits": 3},
            {"code": "CCS355", "name": "Neural Networks and Deep Learning", "type": "theory", "credits": 3},
            {"code": "CS3651", "name": "Cloud Computing", "type": "theory", "credits": 3},
            {"code": "CCS358", "name": "Elective - Perception and Autonomous Navigation", "type": "theory", "credits": 3},
            {"code": "CCS366", "name": "Software Testing", "type": "lab", "credits": 2},
            {"code": "CS3611", "name": "IoT Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 7, "subjects": [
            {"code": "CCS712", "name": "Big Data Analytics", "type": "theory", "credits": 3},
            {"code": "CCS711", "name": "Information Security", "type": "theory", "credits": 3},
            {"code": "CS3751", "name": "Human Computer Interaction", "type": "theory", "credits": 3},
            {"code": "GE3791", "name": "Internship / Industrial Training", "type": "lab", "credits": 2},
            {"code": "CCS799", "name": "Project Phase 1", "type": "lab", "credits": 5},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2021", "semester": 8, "subjects": [
            {"code": "CCS899", "name": "Project Phase 2", "type": "lab", "credits": 10},
            {"code": "EL3811", "name": "Professional Elective", "type": "theory", "credits": 3},
            {"code": "EL3812", "name": "Open Elective", "type": "theory", "credits": 3},
        ]},

        # ═══════════════════════════════════════
        # B.E CSE — Regulation 2025
        # ═══════════════════════════════════════
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 1, "subjects": [
            {"code": "MA1101", "name": "Engineering Mathematics I", "type": "theory", "credits": 4},
            {"code": "PH1101", "name": "Physics for Engineers", "type": "theory", "credits": 3},
            {"code": "CS1101", "name": "Computational Thinking with Python", "type": "theory", "credits": 3},
            {"code": "EE1101", "name": "Basic Electrical Engineering", "type": "theory", "credits": 3},
            {"code": "HS1101", "name": "Technical English", "type": "theory", "credits": 2},
            {"code": "CS1111", "name": "Python Programming Lab", "type": "lab", "credits": 2},
            {"code": "PH1111", "name": "Physics Lab", "type": "lab", "credits": 1},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 2, "subjects": [
            {"code": "MA1201", "name": "Engineering Mathematics II", "type": "theory", "credits": 4},
            {"code": "CY1201", "name": "Chemistry for Engineers", "type": "theory", "credits": 3},
            {"code": "CS1201", "name": "Data Structures with C", "type": "theory", "credits": 3},
            {"code": "EC1201", "name": "Digital Logic Design", "type": "theory", "credits": 3},
            {"code": "ME1201", "name": "Engineering Graphics & CAD", "type": "theory", "credits": 3},
            {"code": "CS1211", "name": "Data Structures Lab", "type": "lab", "credits": 2},
            {"code": "CY1211", "name": "Chemistry Lab", "type": "lab", "credits": 1},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 3, "subjects": [
            {"code": "MA2301", "name": "Probability and Statistics", "type": "theory", "credits": 4},
            {"code": "CS2301", "name": "Object Oriented Programming with Java", "type": "theory", "credits": 3},
            {"code": "CS2302", "name": "Computer Organization & Architecture", "type": "theory", "credits": 4},
            {"code": "CS2303", "name": "Discrete Structures", "type": "theory", "credits": 3},
            {"code": "CS2304", "name": "Database Systems", "type": "theory", "credits": 3},
            {"code": "CS2311", "name": "Java Programming Lab", "type": "lab", "credits": 2},
            {"code": "CS2312", "name": "Database Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 4, "subjects": [
            {"code": "CS2401", "name": "Design and Analysis of Algorithms", "type": "theory", "credits": 4},
            {"code": "CS2402", "name": "Operating Systems", "type": "theory", "credits": 3},
            {"code": "CS2403", "name": "Software Engineering", "type": "theory", "credits": 3},
            {"code": "CS2404", "name": "Artificial Intelligence", "type": "theory", "credits": 3},
            {"code": "CS2405", "name": "Web Technologies", "type": "theory", "credits": 3},
            {"code": "CS2411", "name": "Algorithm Design Lab", "type": "lab", "credits": 2},
            {"code": "CS2412", "name": "Web Development Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 5, "subjects": [
            {"code": "CS3501R", "name": "Computer Networks", "type": "theory", "credits": 4},
            {"code": "CS3502", "name": "Machine Learning", "type": "theory", "credits": 3},
            {"code": "CS3503", "name": "Theory of Computation", "type": "theory", "credits": 3},
            {"code": "CS3504", "name": "Cloud Computing", "type": "theory", "credits": 3},
            {"code": "CS3505", "name": "Elective I", "type": "theory", "credits": 3},
            {"code": "CS3511R", "name": "Networks Lab", "type": "lab", "credits": 2},
            {"code": "CS3512", "name": "Machine Learning Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 6, "subjects": [
            {"code": "CS3601", "name": "Deep Learning", "type": "theory", "credits": 3},
            {"code": "CS3602", "name": "Cyber Security", "type": "theory", "credits": 3},
            {"code": "CS3603", "name": "Distributed Systems", "type": "theory", "credits": 3},
            {"code": "CS3604", "name": "Elective II", "type": "theory", "credits": 3},
            {"code": "CS3605", "name": "Elective III", "type": "theory", "credits": 3},
            {"code": "CS3611R", "name": "Deep Learning Lab", "type": "lab", "credits": 2},
            {"code": "CS3612", "name": "Mini Project", "type": "lab", "credits": 2},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 7, "subjects": [
            {"code": "CS4701", "name": "Elective IV", "type": "theory", "credits": 3},
            {"code": "CS4702", "name": "Elective V", "type": "theory", "credits": 3},
            {"code": "CS4711", "name": "Internship", "type": "lab", "credits": 4},
            {"code": "CS4712", "name": "Project Phase 1", "type": "lab", "credits": 5},
        ]},
        {"degree": "B.E/B.Tech", "regulation": "Regulation 2025", "semester": 8, "subjects": [
            {"code": "CS4801", "name": "Project Phase 2", "type": "lab", "credits": 10},
            {"code": "CS4802", "name": "Open Elective", "type": "theory", "credits": 3},
            {"code": "CS4803", "name": "Comprehensive Viva", "type": "theory", "credits": 2},
        ]},

        # ═══════════════════════════════════════
        # BSc Computer Science — Regulation 2021
        # ═══════════════════════════════════════
        {"degree": "BSc", "regulation": "Regulation 2021", "semester": 1, "subjects": [
            {"code": "BSC101", "name": "Programming Fundamentals", "type": "theory", "credits": 4},
            {"code": "BSC102", "name": "Mathematics I", "type": "theory", "credits": 4},
            {"code": "BSC103", "name": "Digital Electronics", "type": "theory", "credits": 3},
            {"code": "BSC104", "name": "English Communication", "type": "theory", "credits": 2},
            {"code": "BSC111", "name": "Programming Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "BSc", "regulation": "Regulation 2021", "semester": 2, "subjects": [
            {"code": "BSC201", "name": "Data Structures", "type": "theory", "credits": 4},
            {"code": "BSC202", "name": "Mathematics II", "type": "theory", "credits": 4},
            {"code": "BSC203", "name": "Computer Organization", "type": "theory", "credits": 3},
            {"code": "BSC204", "name": "Environmental Studies", "type": "theory", "credits": 2},
            {"code": "BSC211", "name": "Data Structures Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "BSc", "regulation": "Regulation 2021", "semester": 3, "subjects": [
            {"code": "BSC301", "name": "Object Oriented Programming", "type": "theory", "credits": 4},
            {"code": "BSC302", "name": "Operating Systems", "type": "theory", "credits": 3},
            {"code": "BSC303", "name": "Database Management Systems", "type": "theory", "credits": 3},
            {"code": "BSC304", "name": "Statistics", "type": "theory", "credits": 3},
            {"code": "BSC311", "name": "DBMS Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "BSc", "regulation": "Regulation 2021", "semester": 4, "subjects": [
            {"code": "BSC401", "name": "Web Technologies", "type": "theory", "credits": 4},
            {"code": "BSC402", "name": "Computer Networks", "type": "theory", "credits": 3},
            {"code": "BSC403", "name": "Software Engineering", "type": "theory", "credits": 3},
            {"code": "BSC404", "name": "Numerical Methods", "type": "theory", "credits": 3},
            {"code": "BSC411", "name": "Web Development Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "BSc", "regulation": "Regulation 2021", "semester": 5, "subjects": [
            {"code": "BSC501", "name": "Python Programming", "type": "theory", "credits": 4},
            {"code": "BSC502", "name": "Machine Learning Basics", "type": "theory", "credits": 3},
            {"code": "BSC503", "name": "Cloud Computing", "type": "theory", "credits": 3},
            {"code": "BSC504", "name": "Elective I", "type": "theory", "credits": 3},
            {"code": "BSC511", "name": "Python Lab", "type": "lab", "credits": 2},
        ]},
        {"degree": "BSc", "regulation": "Regulation 2021", "semester": 6, "subjects": [
            {"code": "BSC601", "name": "Project", "type": "lab", "credits": 8},
            {"code": "BSC602", "name": "Elective II", "type": "theory", "credits": 3},
            {"code": "BSC603", "name": "Cyber Security", "type": "theory", "credits": 3},
            {"code": "BSC604", "name": "Internship", "type": "lab", "credits": 4},
        ]},

        # ═══════════════════════════════════════
        # BCom — Regulation 2021
        # ═══════════════════════════════════════
        {"degree": "BCom", "regulation": "Regulation 2021", "semester": 1, "subjects": [
            {"code": "BC101", "name": "Financial Accounting I", "type": "theory", "credits": 4},
            {"code": "BC102", "name": "Business Economics", "type": "theory", "credits": 3},
            {"code": "BC103", "name": "Business Organization", "type": "theory", "credits": 3},
            {"code": "BC104", "name": "Business Communication", "type": "theory", "credits": 2},
            {"code": "BC105", "name": "Computer Applications", "type": "theory", "credits": 3},
        ]},
        {"degree": "BCom", "regulation": "Regulation 2021", "semester": 2, "subjects": [
            {"code": "BC201", "name": "Financial Accounting II", "type": "theory", "credits": 4},
            {"code": "BC202", "name": "Business Mathematics", "type": "theory", "credits": 3},
            {"code": "BC203", "name": "Marketing Management", "type": "theory", "credits": 3},
            {"code": "BC204", "name": "Business Law", "type": "theory", "credits": 3},
            {"code": "BC205", "name": "Environmental Studies", "type": "theory", "credits": 2},
        ]},
        {"degree": "BCom", "regulation": "Regulation 2021", "semester": 3, "subjects": [
            {"code": "BC301", "name": "Corporate Accounting", "type": "theory", "credits": 4},
            {"code": "BC302", "name": "Business Statistics", "type": "theory", "credits": 3},
            {"code": "BC303", "name": "Banking and Insurance", "type": "theory", "credits": 3},
            {"code": "BC304", "name": "Cost Accounting", "type": "theory", "credits": 3},
            {"code": "BC305", "name": "Company Law", "type": "theory", "credits": 3},
        ]},
        {"degree": "BCom", "regulation": "Regulation 2021", "semester": 4, "subjects": [
            {"code": "BC401", "name": "Income Tax", "type": "theory", "credits": 4},
            {"code": "BC402", "name": "Management Accounting", "type": "theory", "credits": 3},
            {"code": "BC403", "name": "Human Resource Management", "type": "theory", "credits": 3},
            {"code": "BC404", "name": "Financial Management", "type": "theory", "credits": 3},
            {"code": "BC405", "name": "E-Commerce", "type": "theory", "credits": 3},
        ]},
        {"degree": "BCom", "regulation": "Regulation 2021", "semester": 5, "subjects": [
            {"code": "BC501", "name": "Indirect Taxation (GST)", "type": "theory", "credits": 4},
            {"code": "BC502", "name": "Auditing", "type": "theory", "credits": 3},
            {"code": "BC503", "name": "Entrepreneurship Development", "type": "theory", "credits": 3},
            {"code": "BC504", "name": "Elective I", "type": "theory", "credits": 3},
            {"code": "BC505", "name": "International Business", "type": "theory", "credits": 3},
        ]},
        {"degree": "BCom", "regulation": "Regulation 2021", "semester": 6, "subjects": [
            {"code": "BC601", "name": "Project / Internship", "type": "lab", "credits": 6},
            {"code": "BC602", "name": "Financial Services", "type": "theory", "credits": 3},
            {"code": "BC603", "name": "Elective II", "type": "theory", "credits": 3},
            {"code": "BC604", "name": "Indian Economy", "type": "theory", "credits": 3},
        ]},
    ]


async def seed_database(db):
    """Seed the database with curriculum data."""
    data = get_seed_data()
    
    existing = await db.curriculum.count_documents({})
    if existing > 0:
        print(f"Warning: Database already has {existing} curriculum records. Skipping seed.")
        return existing

    result = await db.curriculum.insert_many(data)
    count = len(result.inserted_ids)
    print(f"Seeded {count} curriculum records")
    return count
