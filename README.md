🚀 SkillBridge — AI-Powered Career Guidance

SkillBridge is an AI-powered career guidance platform that helps users identify suitable job opportunities, discover missing skills, and receive personalized course recommendations based on their skills and career interests.

🎯 Problem Statement

Many students and job seekers struggle to understand which jobs match their current skills and what additional skills they need to develop. SkillBridge addresses this problem by providing personalized, AI-driven career guidance.

✨ Key Features

- AI Profile Analysis: Extracts relevant skills and career information from user input.
- Intelligent Job Matching: Matches users with suitable job opportunities using semantic similarity.
- Skill Gap Analysis: Identifies skills that users need to improve.
- Personalized Course Recommendations: Suggests courses to help users bridge their skill gaps.
- Interactive Web Interface: Simple and user-friendly dark-themed frontend.
- FastAPI Backend: Provides an API for processing user profiles and generating recommendations.

🛠️ Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- AI Workflow: LangGraph
- LLM: Groq API
- Machine Learning: Sentence Transformers
- Model: "all-MiniLM-L6-v2"
- Version Control: Git and GitHub

🏗️ Project Architecture

User
  │
  ▼
Frontend
(HTML, CSS, JavaScript)
  │
  ▼
FastAPI Backend
  │
  ▼
LangGraph Pipeline
  │
  ├── Profile Parser
  │
  ├── Job Matcher
  │
  ├── Skill Gap Analyzer
  │
  └── Course Recommender
  │
  ▼
Personalized Career Results
  ├── Matched Jobs
  ├── Skill Gaps
  └── Recommended Courses

📁 Project Structure

SkillGapAgent/
│
├── agents/
│   ├── profile_parser.py
│   ├── job_matcher.py
│   ├── gap_analyzer.py
│   ├── recommender.py
│   └── graph.py
│
├── api/
│   └── main.py
│
├── data/
│   └── jobs.json
│
├── models/
│   └── schemas.py
│
├── frontend/
│   └── index.html
│
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Installation and Setup

1. Clone the repository

git clone https://github.com/nayana12434/SkillGapAgent.git
cd SkillGapAgent

2. Create a virtual environment

python -m venv .venv

Activate the environment on Windows:

.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure the API key

Create a ".env" file in the project root:

GROQ_API_KEY=your_groq_api_key_here

«Never upload your ".env" file or expose your API key publicly.»

▶️ Running the Application

1. Start the backend

Run this command from the project root:

uvicorn api.main:app --reload

The backend will run at:

http://127.0.0.1:8000

2. Open the frontend

Open the following file in a browser using the Live Server extension in VS Code:

frontend/index.html

3. Use SkillBridge

1. Enter your skills, education, or career interests.
2. Click Analyze Profile.
3. View your matched jobs, skill gaps, and recommended courses.

🔐 Security

- API keys are stored in environment variables.
- The ".env" file is excluded using ".gitignore".
- Users should use their own Groq API key when running the project locally.

🔮 Future Enhancements

- User authentication and profile management
- Real-time job listings from external APIs
- More comprehensive course databases
- Resume upload and analysis
- Progress tracking for skill development
- Integration with professional networking platforms

👥 Team

Developed as a hackathon project to provide accessible and personalized AI-powered career guidance.

📄 License

This project is intended for educational and hackathon purposes.