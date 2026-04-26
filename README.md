<br />
<div align="center">
  <h1 align="center">🎓 Jensy — Academic Companion</h1>
  <p align="center">
    <strong>A personalized, AI-powered academic platform built for bachelor's degree students.</strong>
    <br />
    <br />
    <a href="#features">Features</a> &middot;
    <a href="#tech-stack">Tech Stack</a> &middot;
    <a href="#getting-started">Getting Started</a>
  </p>
</div>

<hr />

## 🌟 About The Project

Jensy is a full-stack, end-to-end platform tailored to bachelor's degree students. It tracks academic progress, offers 8-semester dashboards, manages study resources, and features an **AI Assistant** capable of behavioral profiling and academic planning. Instead of just answering questions, Jensy adapts its tone based on the student's learning preference (e.g., Coding Track vs. Non-Coding Track) and proactively extracts intents and deadlines from your messages using **spaCy**.

Whether you're from an autonomous college (with live syllabus scraping) or an affiliated university, Jensy intelligently maps out your academic journey.

## ✨ Features

- 🎒 **Intelligent Onboarding**: Multi-step wizard mapping you to the right curriculum based on your college regulation or scraping it directly via URLs for autonomous colleges.
- 📊 **Dynamic 8-Semester Dashboard**: Visualize your entire bachelor's journey. Track progress bars for theory, labs, and credits at a glance.
- 🤖 **Behavioral AI Assistant**: Powered by **GPT-4o** and **spaCy NER**, the AI extracts deadlines, flags weak subjects, and delivers personalized advice dynamically catering to coders vs. theory learners.
- 📚 **Syllabus & Resource Hub**: Per-subject repository for downloading and uploading notes, syllabus, and past-year question papers (PYQs). Let the community share knowledge instantly!
- 🔒 **Secure Authorization**: Complete JWT-based authentication flow with Refresh Tokens and Role-Based Access Control (Admin/Student).
- 🎮 **Gamification System**: Earn XP, build streaks, and collect badges for completing subjects and interacting with the AI.
- 📅 **AI Study Planner**: Generate personalized weekly study schedules with a beautiful Calendar visualization.
- 📄 **RAG PDF Summarizer**: Upload course PDFs and ask the AI specific questions based on the document's context using ChromaDB and PyMuPDF.
- 📈 **Learning Analytics**: Visual dashboard using Recharts to track your XP growth, chat frequency, and completed subjects.
- 💼 **Career Builder**: Autonomously generate a Markdown Resume and 10 Mock Interview Q&As based on your completed subjects.
- 🗳️ **Peer Resource Voting**: Upvote and downvote community resources.
- 📱 **Progressive Web App (PWA)**: Install Jensy on your device with offline caching and background service workers.
- 🛡️ **Rate Limiting & Quotas**: Built-in API cost guards and daily AI token quotas tracked in real-time.
- ⏰ **Automated Scraper**: Background APScheduler cron jobs keep your syllabus up-to-date and notify you of any changes.


## 💻 Tech Stack

- **Frontend**: React (Vite) + Vanilla CSS (Glassmorphism & Micro-animations)
- **Backend**: Python FastAPI (High-performance Async APIs)
- **Database**: MongoDB (via Motor for asynchronous DB transactions)
- **AI / NLP**: OpenAI API (`gpt-4o`) + **spaCy** (NER & Intent pipelines)
- **Tooling**: `axios`, `beautifulsoup4` (Scraping), `apscheduler` (Cron Jobs)

## 📁 Folder Structure

```text
jensy/
├── frontend/                   # React PWA application (Vite ecosystem)
│   ├── public/                 # Static assets
│   │   ├── manifest.json       # PWA manifest for offline caching
│   │   └── service-worker.js   # Background service worker caching logic
│   ├── src/
│   │   ├── api/                # Axios API connection to FastAPI endpoints
│   │   ├── components/         # Reusable UI elements (Navbar, Badges)
│   │   ├── context/            # React Context providers (AuthContext)
│   │   ├── pages/              # View Components:
│   │   │   ├── AIChat          # AI interaction with Quota & Behavior reports
│   │   │   ├── Analytics       # Learning analytics using Recharts
│   │   │   ├── Career          # GPT-4o Resume & Mock Interview generator
│   │   │   ├── Dashboard       # 8-Semester academic tracking & Gamification
│   │   │   ├── Planner         # AI Study Planner & react-big-calendar view
│   │   │   └── Resources       # Subject notes, PDFs, and peer voting hub
│   │   └── index.css           # Global CSS tokens and variables
│   └── package.json            # Frontend dependencies
├── backend/                    # Python FastAPI Engine
│   ├── db/                     # Motor async MongoDB & ChromaDB managers
│   ├── models/                 # Pydantic Schemas:
│   │   ├── student.py          # User, Behavior Profile, XP & Token Quotas
│   │   ├── attendance.py       # Attendance & Internal Marks models
│   │   └── resource.py         # Notes & PDF schema with Upvote/Downvote
│   ├── routes/                 # REST API Routers:
│   │   ├── admin.py            # Aggregation endpoints for staff overview
│   │   ├── ai.py               # Rate-limited GPT-4o chat handler
│   │   ├── analytics.py        # Chart data aggregation routes
│   │   └── planner.py          # Exam study schedule generator
│   ├── services/               # Core Logic Systems:
│   │   ├── ai_engine.py        # System prompts & GPT communication
│   │   ├── gamification.py     # XP, streak calculations, and badges
│   │   ├── rag.py              # PyMuPDF extraction & ChromaDB queries
│   │   └── scheduler.py        # APScheduler autonomous syllabus scraper
│   ├── utils/                  # Auth dependency & SlowAPI rate limiting
│   ├── main.py                 # Uvicorn application lifecycle & routers
│   └── requirements.txt        # Backend dependencies
└── .env                        # Environment configurations
```


## 🚀 Getting Started

To get a local copy up and running locally, follow these simple steps.

### Prerequisites

Make sure you have Node.js (`npm`), Python (`pip`), and access to a MongoDB cluster installed on your system.

### Installation

1. **Clone the repo**
   ```sh
   git clone https://github.com/your-username/Jensy.git
   cd Jensy
   ```

2. **Setup Background Services & Environment Variables**
   Create a `.env` file in the root directory and add the following:
   ```env
   MONGO_URI=mongodb://localhost:27017
   JWT_SECRET=your_secret_key_here
   OPENAI_API_KEY=sk-your-openai-key
   FRONTEND_URL=http://localhost:5173
   ```

3. **Install Backend Dependencies**
   ```sh
   cd backend
   pip install -r requirements.txt
   
   # Download the required spaCy model for NER
   python -m spacy download en_core_web_sm
   ```

4. **Install Frontend Dependencies**
   ```sh
   cd ../frontend
   npm install
   ```

5. **Seed the Database** (Optional but recommended)
   Populates your MongoDB instance with real engineering syllabus data (Regulation 2021 & 2025).
   ```sh
   cd ../backend
   python services/seed.py
   ```

### Running the App

Start both servers in separate terminal instances:

**Run the Backend Engine:**
```sh
cd backend
python -m uvicorn main:app --reload --port 8000
```
> Explore the live FastAPI docs at `http://localhost:8000/docs`

**Run the Frontend Client:**
```sh
cd frontend
npm run dev
```
> Launch the platform at `http://localhost:5173/`


## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
