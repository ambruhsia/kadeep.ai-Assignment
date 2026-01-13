# InternHub - Quick Reference Card

## 🚀 Quick Start (2 minutes)

```bash
cd InternHub
pip install -r requirements.txt
python cli.py
# Choose option 4 for full analysis
```

## 📌 What This Does

**InternHub** matches students to internships using:
1. **Match Score** (0-1.0) - How well they fit
2. **Skill Gaps** - What they need to learn
3. **Optimized Resume** - AI-generated, JD-specific
4. **ATS Score** (%) - Will it pass screening?

## 🎯 Example Usage

### CLI Mode
```bash
python cli.py

Option 4: Full analysis
├─ Match Analysis: 78%
├─ Skill Gaps: Docker, AWS
├─ Optimized Resume: [Generated]
└─ ATS Score: 80%
```

### API Mode
```bash
python app.py
# POST http://localhost:5000/full-analysis
# Body: {"student": {...}, "job": {...}}
```

### Python Code
```python
from ai_agent import analyze_internship_fit
from student_profile import StudentProfile
from internship_job import InternshipJob

student = StudentProfile(
    name="Rajesh", skills=["Python", "JavaScript"],
    interests=["Web Dev"], experience="3 projects", cgpa=3.6
)

job = InternshipJob(
    title="Full Stack Developer",
    company="TechCorp",
    required_skills=["Python", "JavaScript", "React"],
    # ... more fields
)

result = analyze_internship_fit(student, job)
print(result['confidence_score'])  # 0.78
```

## 📊 Understanding the Output

### Match Score Meaning
- **0.7+** → ✅ Strong fit, apply immediately
- **0.5-0.7** → ⚠️ Decent fit, upskill first
- **<0.5** → 🔴 Challenge fit, heavy prep needed

### Skill Gaps Action Items
- **Database Design** → Learn SQL, Normalization
- **Docker** → Take container course
- **AWS** → Complete AWS fundamentals

### Resume
- AI-generated from template
- Highlights job-relevant skills
- ATS-optimized (no fancy formatting)

### ATS Score
- **80%+** → Will likely pass ATS
- **60-80%** → Should be OK
- **<60%** → Might get filtered
- **Tip**: Add missing keywords to resume

## 🔑 Core Algorithms

### Match Score Formula
```
Score = (Required Skills × 0.6) + (Preferred × 0.3) 
      + (Interests × 0.2) + (CGPA × 0.1)
```

### Skill Gaps
```
Gaps = Required Skills - Student Skills
```

### ATS Score
```
Score = Matched Keywords / Total Keywords
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `ai_agent.py` | Core matching logic |
| `cli.py` | Interactive tool |
| `app.py` | Web API |
| `config.py` | Settings |

## 💻 Commands

```bash
# Interactive mode
python cli.py

# Quick demo
python cli.py --quick-test

# Full test suite
python test_internhub.py

# Start API server
python app.py

# Load JSON files
# In CLI, choose option 5
```

## 🧠 How AI Works

**No Complex ML!** Uses:
1. **Smart Prompts** - Instruction-based text generation
2. **Simple Scoring** - Weighted algorithms
3. **Keyword Matching** - Find relevant skills
4. **Template Fallback** - Works without API key

## 🔌 Using Real LLM (Optional)

1. Get OpenAI API key
2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. Change `config.py`:
   ```python
   USE_MOCK_LLM = False
   ```

Done! System now uses real GPT-4 API.

## 🧪 Testing

```bash
python test_internhub.py
# Runs 6 test cases:
# 1. Strong full-stack match
# 2. Beginner for backend role
# 3. Resume generation
# 4. ATS scoring
# 5. Full pipeline
# 6. JSON serialization
```

## 📚 Documentation

| Doc | Purpose |
|-----|---------|
| `README.md` | Complete guide |
| `QUICKSTART.md` | Quick setup |
| `ARCHITECTURE.md` | Technical deep dive |
| `IMPLEMENTATION_SUMMARY.md` | What was built |

## 🎯 Use Cases

### 1. Student Perspective
"Should I apply?"
→ Match Score tells them fit level

### 2. Student Skill Planning
"What should I learn?"
→ Skill Gaps shows what to upskill

### 3. Resume Optimization
"Will my resume pass ATS?"
→ ATS Score + keyword analysis

### 4. Career Advisor
"Which roles fit this student?"
→ Run analysis on multiple jobs

## ⚡ Performance

- Match analysis: <50ms
- Resume generation: ~50ms (mock) or 1-3s (real API)
- ATS calculation: <5ms
- Full pipeline: <100ms (mock)

## 🔐 What's NOT Included

❌ Database (can add easily)
❌ User authentication
❌ Application tracking
❌ Email notifications
❌ Interview scheduling

✅ Everything else is there!

## 🎓 Learning Outcomes

Study this code to learn:
- **Prompt engineering** for LLMs
- **Algorithm design** for scoring/matching
- **API design** patterns
- **CLI development** best practices
- **Data modeling** with Python

## 📞 Troubleshooting

**Q: "python command not found"**
A: Use: `python.exe` or install Python

**Q: "ImportError"**
A: Run: `pip install -r requirements.txt`

**Q: "API not responding"**
A: Check: `python app.py` is running on port 5000

**Q: "Mock LLM generating weird text"**
A: Normal! Add real API key for better quality

## 🚀 Next Steps

1. Try the CLI: `python cli.py`
2. Run tests: `python test_internhub.py`
3. Start API: `python app.py`
4. Read code: Start with `ai_agent.py`
5. Customize: Edit prompts in `ai_agent.py`

---

**InternHub: Make internship matching intelligent!** 🎓
