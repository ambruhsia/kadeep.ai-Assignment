# InternHub - AI-Powered Internship Matching Platform

## 🎯 Project Overview

InternHub is a lightweight AI-powered platform that helps students find the right internships and optimize their applications. It uses smart prompt-based reasoning to:

1. **Match Students to Internships** - Calculate compatibility scores
2. **Analyze Skill Gaps** - Identify what skills need improvement
3. **Generate Optimized Resumes** - Create JD-specific resumes using prompt engineering
4. **Calculate ATS Scores** - Ensure resumes pass Applicant Tracking Systems

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────┐
│       InternHub AI Platform             │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ Student      │  │ Internship   │   │
│  │ Profile      │  │ Job Desc     │   │
│  └──────┬───────┘  └──────┬───────┘   │
│         │                  │           │
│         └──────────┬───────┘           │
│                    │                   │
│            ┌───────▼────────┐          │
│            │  InternHubAI   │          │
│            │   Agent        │          │
│            └───────┬────────┘          │
│                    │                   │
│    ┌───────────────┼───────────────┐   │
│    │               │               │   │
│ ┌──▼──┐ ┌─────▼──┐ ┌──▼──┐ ┌─────▼──┐│
│ │Match│ │  Skill │ │Resume│ │ ATS   ││
│ │Score│ │  Gaps  │ │  Gen │ │ Score ││
│ └─────┘ └────────┘ └──────┘ └───────┘│
│                                         │
│    ┌────────────┐      ┌───────────┐  │
│    │  CLI Tool  │      │ Flask API │  │
│    └────────────┘      └───────────┘  │
└─────────────────────────────────────────┘
```
cli ss:
<img width="1202" height="866" alt="image" src="https://github.com/user-attachments/assets/4f35fb7b-24fa-4c15-89d7-fa9bc4969dc8" />
<img width="1210" height="914" alt="image" src="https://github.com/user-attachments/assets/dbe89b9f-bfbb-4afe-8925-12c084ad50a1" />
<img width="1163" height="587" alt="image" src="https://github.com/user-attachments/assets/f0638586-701b-4de9-880e-ccc726cd2c05" />



## 🔑 Core Concepts

### 1. **Match Scoring Algorithm**
Calculates how well a student fits an internship:
- **Skill Coverage (60%)**: Required skill overlap
- **Preferred Skills (30%)**: Match with preferred skills
- **Interest Alignment (20%)**: Interests align with job domain
- **CGPA Factor (10%)**: Academic performance weight

**Formula**: Match Score = (Required Skills × 0.6) + (Preferred Skills × 0.3) + (Interest Match × 0.2) + (CGPA × 0.1)

### 2. **Skill Gap Analysis**
Identifies missing critical skills:
- Compares student skills against required skills
- Categorizes gaps (Programming Language, Framework, Cloud, etc.)
- Prioritizes by importance

### 3. **Resume Generation via Prompts**
Uses LLM prompt engineering to:
- Extract key responsibilities from JD
- Reframe student experience for relevance
- Highlight aligned skills
- Create ATS-friendly formatting

**Key Prompt Strategy**:
```
Context: Student skills, interests, experience
Target: Job requirements, responsibilities, technologies
Output: Resume tailored to maximize relevance
```

### 4. **ATS (Applicant Tracking System) Score**
Measures resume-to-JD alignment:
- Keyword matching (required + preferred skills)
- Score = Matched Keywords / Total Keywords
- Identifies gaps for improvement

## 📁 Project Structure

```
InternHub/
├── config.py                 # Configuration, API keys, settings
├── student_profile.py        # StudentProfile data model
├── internship_job.py         # InternshipJob data model
├── ai_agent.py              # Core AI matching engine
├── cli.py                   # Command-line interface
├── app.py                   # Flask REST API
├── requirements.txt         # Python dependencies
├── example_data/
│   ├── examples.py          # Example student & job data
│   ├── student.json         # Sample student profile
│   └── job.json             # Sample internship JD
└── README.md                # This file
```

## 🚀 How to Run

### Option 1: CLI Tool (Interactive)

```bash
# 1. Install dependencies
pip install -r requirements.txt

```
### Option 2: Flask API (Web Service)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start API server
python app.py

# 3. Access API at http://localhost:5000
#    - GET  / → API documentation
#    - POST /analyze → Match analysis
#    - POST /resume → Resume generation
#    - POST /ats → ATS scoring
#    - POST /full-analysis → Complete analysis
```

### Option 3: Quick Test

```bash
python cli.py --quick-test
```


## 📊 Example Usage

### CLI Example (Interactive):

```
🎓 INTERNHUB - AI-Powered Internship Matching

What would you like to do?
1. Analyze internship fit
2. Generate optimized resume
3. Get ATS score
4. Full analysis (all features)
5. Load from JSON files
6. Exit

Enter your choice: 4

📝 Enter Student Profile:
  Full Name: Rajesh Kumar
  Email: rajesh@example.com
  Skills: Python, JavaScript, React, Flask, REST APIs
  Interests: Web Development, Backend
  Experience: Built 3 projects
  CGPA: 3.6

💼 Enter Internship Job Details:
  Job Title: Full Stack Developer Intern
  Company: TechCorp
  ...

⏳ Running full analysis...

✨ MATCH SCORE: 0.78/1.0 (78%)
✅ STRONG FIT

💪 Strengths:
  ✓ Strong in Python (aligns with Required skill)
  ✓ Strong in Flask (aligns with Required skill)

🔧 Skill Gaps to Address:
  • Database Design (Technical Skill)

📄 OPTIMIZED RESUME:
[AI-generated resume optimized for the JD]

🤖 ATS SCORE: 80% (0.8/1.0)
  Matched keywords: 4/5

📊 FINAL RECOMMENDATION:
Match Score: 0.78/1.0
ATS Score: 80%
Recommendation: ✅ APPLY
```

### API Example (POST /full-analysis):

**Request**:
```json
{
  "student": {
    "name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "skills": ["Python", "JavaScript", "React", "Flask"],
    "interests": ["Web Development", "Backend"],
    "experience": "Built 3 full-stack projects",
    "cgpa": 3.6,
    "resume_text": ""
  },
  "job": {
    "title": "Full Stack Developer Intern",
    "company": "TechCorp",
    "description": "Build scalable web applications...",
    "required_skills": ["Python", "JavaScript", "React"],
    "preferred_skills": ["Docker", "AWS"],
    "responsibilities": ["Develop features", "Write tests"],
    "duration_months": 3,
    "location": "Remote"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "student_name": "Rajesh Kumar",
    "job_title": "Full Stack Developer Intern",
    "company": "TechCorp",
    "match_analysis": {
      "confidence_score": 0.78,
      "match_percentage": "78%",
      "is_match": true,
      "skill_gaps": [
        {
          "skill": "Docker",
          "category": "Cloud Platform",
          "importance": "Required"
        }
      ],
      "strengths": [
        "Strong in Python (aligns with Required skill)",
        "Strong in React (aligns with Required skill)"
      ],
      "recommendation": "This student is a strong fit..."
    },
    "optimized_resume": "[Generated resume text]",
    "ats_score": {
      "ats_score": 0.8,
      "ats_percentage": "80%",
      "matched_keywords": ["Python", "JavaScript", "React"],
      "missing_keywords": ["Docker"],
      "keyword_count": 4,
      "matched_count": 3
    }
  }
}
```

## 🤖 AI Features & Prompt Design

### 1. **Match Recommendation Prompts**

The system uses contextual prompts to generate personalized recommendations:

```python
"""
Student Profile Context:
- Name, Skills, Interests, Experience, CGPA

Job Context:
- Title, Company, Requirements, Responsibilities

Prompt Template:
"You are a career advisor. Given this student's profile and this job,
provide a 2-3 sentence recommendation on whether they should apply.
Consider skill gaps and match percentage. Be encouraging but honest."
```

This produces natural-language recommendations instead of generic text.

### 2. **Resume Generation Prompts**

Creates JD-optimized resumes through instruction-based generation:

```python
"""
Prompt:
"Generate a professional resume for [Student] tailored to [Job Title] at [Company].
Emphasize skills: [Required Skills]
Keep it under 300 words, ATS-friendly format."

Key Strategy:
- Extract job-specific skills
- Reframe experience to highlight relevance
- Use keywords from JD
- Maintain ATS-friendly formatting
"""
```

### 3. **Fallback Mock LLM**

When real API is unavailable, uses intelligent mock responses:
- Pattern matching on prompt intent
- Context-aware response templates
- Prevents disruption to user workflow

## 📈 Key Metrics Explained

### **Confidence Score (Match Score)**
- Range: 0.0 - 1.0
- **0.7+**: Strong fit, apply immediately
- **0.5-0.7**: Decent fit, consider upskilling
- **<0.5**: Challenge fit, prepare well

### **ATS Score**
- Range: 0% - 100%
- Percentage of job keywords found in resume
- **80%+**: Likely to pass ATS scanning
- **<60%**: May be filtered out by ATS

### **Skill Gap Count**
- Number of critical missing skills
- Prioritized by job requirement level
- Actionable improvement guide

## 🔧 Configuration

Edit `config.py` to customize:

```python
USE_MOCK_LLM = True  # Set False for real OpenAI API
OPENAI_API_KEY = "your-key-here"
CONFIDENCE_THRESHOLD = 0.5  # Match threshold
MAX_SKILL_GAPS = 5  # Gaps to show
```

## 📦 Dependencies

- `python-dotenv`: Environment variable management
- `requests`: HTTP requests (for potential API calls)
- `flask`: REST API framework

## 🎓 Learning Outcomes

By studying this codebase, you'll understand:

1. **Prompt Engineering**: How to design effective LLM prompts
2. **Data Modeling**: Clean separation of concerns (Student, Job, Agent)
3. **Algorithm Design**: Scoring algorithms for matching
4. **API Design**: RESTful architecture
5. **CLI Development**: User-friendly command-line interfaces
6. **LLM Integration**: Working with AI APIs (real or mock)

## 🚧 Future Enhancements

- [ ] Real OpenAI/Claude API integration
- [ ] Batch processing for multiple candidates
- [ ] Interview prep suggestions
- [ ] Salary negotiation tips
- [ ] Company research module
- [ ] Application tracking
- [ ] Interview scheduling
- [ ] Feedback loop for continuous improvement

## 📝 Notes

- **No Authentication**: This is a simple demo platform
- **No Database**: All data is in-memory (can be easily added)
- **Mock LLM**: Uses intelligent templates by default (easy OpenAI upgrade)
- **Minimal UI**: Focus is on logic, not design

## 🤝 Contributing

Feel free to:
- Enhance the prompt templates
- Add more data models
- Implement real LLM APIs
- Create a web UI
- Add more analysis features

--- 
