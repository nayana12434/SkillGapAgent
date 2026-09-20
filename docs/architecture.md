# SkillBridge AI Architecture

```mermaid
flowchart TD
    A[User Enters Profile Details] --> B[Frontend - HTML/CSS/JavaScript]
    B --> C[FastAPI Backend]
    C --> D[Profile Parser - Groq LLM]
    D --> E[Structured User Profile]
    E --> F[Embedding-Based Job Matcher]
    F --> G[Skill Gap Analyzer - Groq LLM]
    G --> H[Course Recommendation Module]
    H --> I[Final Career Recommendations]
    I --> B
    B --> J[Display Jobs, Skill Gaps and Courses]
```

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI
- AI Model: Groq LLM
- Job Matching: Sentence Transformers
- Workflow: LangGraph
- Data Validation: Pydantic
- Version Control: GitHub
```s