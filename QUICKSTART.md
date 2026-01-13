# InternHub - Quick Start Guide

## ⚡ 30-Second Setup

```bash
# 1. Navigate to project
cd InternHub

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run CLI
python cli.py

# 4. OR run API
python app.py
```

## 🎯 What This Project Does

**InternHub** is an AI-powered internship matching system that:

1. **Matches students to internships** with confidence scores
2. **Identifies skill gaps** students need to address
3. **Generates optimized resumes** for specific job descriptions
4. **Calculates ATS scores** to ensure resumes pass screening

## 🔄 Workflow

```
Student Profile + Job Description
           ↓
    ┌──────────────────┐
    │  InternHub AI    │
    │    Analysis      │
    └──────────────────┘
           ↓
    ┌──────┬────────┬──────┐
    ↓      ↓        ↓      ↓
  Match  Skills  Resume   ATS
  Score  Gaps     Gen    Score
```

## 📋 Example Scenarios

### Scenario 1: Check Job Fit
```
Input:
  - Rajesh: Python, JavaScript, React, Flask
  - Job: Full Stack Developer (needs Python, JS, React)

Output:
  ✅ 78% match - Strong fit!
  💪 Strengths: Python, JavaScript, React
  🔧 Gap: Docker, AWS
```

### Scenario 2: Optimize Resume
```
Input:
  - Student resume (generic)
  - Target job description

Output:
  📄 ATS-optimized resume tailored to job
  🎯 Highlights relevant experience
  🤖 80% ATS score (passes filtering)
```

## 🧠 How the AI Works

### **No Complex ML Required!**
InternHub uses simple, explainable logic:

1. **Match Score** = Skill overlap + Interest alignment + CGPA
2. **Skill Gaps** = Required skills - Student skills
3. **Resume** = Prompt-based generation using LLM
4. **ATS** = Keyword matching in resume vs JD

### **Prompt-Based AI**
- Uses LLM prompts for intelligent text generation
- Falls back to smart templates (no real API needed)
- Easy to upgrade to real OpenAI/Claude APIs

## 🚀 Running Examples

### CLI Mode
```bash
python cli.py

# Then choose:
# Option 4 → Full analysis
# Option 5 → Load from JSON
```

### API Mode
```bash
python app.py

# Then POST to:
# http://localhost:5000/full-analysis
```

### Quick Test
```bash
python cli.py --quick-test
```

## 📊 Understanding the Output

### Match Analysis
```
✨ MATCH SCORE: 0.78/1.0 (78%)

Explanation:
  - Python: ✅ (required skill)
  - JavaScript: ✅ (required skill)
  - Docker: ❌ (missing, preferred)
```

### Skill Gaps
```
🔧 Skill Gaps to Address:
  • Docker (Cloud Platform)
  • Kubernetes (Cloud Platform)
```

**Action**: Take Docker course before applying

### ATS Score
```
🤖 ATS SCORE: 80% (4/5 keywords matched)

✅ Matched: Python, JavaScript, React, Flask
❌ Missing: Docker
```

**Action**: Add Docker to resume if you learn it

## 🎓 Learning Points

This project demonstrates:

1. **Prompt Engineering**: How to write effective LLM prompts
2. **Scoring Algorithms**: Building match algorithms
3. **API Design**: Clean REST API design
4. **CLI Tools**: Interactive command-line applications
5. **Data Modeling**: Clean data structures
6. **Fallback Systems**: Mock LLM when real API unavailable

## 🔌 Integrating Real LLM

### OpenAI Integration (Optional)

1. Get API key from OpenAI
2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. In `config.py`, set:
   ```python
   USE_MOCK_LLM = False
   ```

That's it! The system will use real OpenAI API.

## 📁 Important Files

| File | Purpose |
|------|---------|
| `ai_agent.py` | Core matching & analysis logic |
| `cli.py` | Interactive command-line tool |
| `app.py` | REST API endpoints |
| `student_profile.py` | Student data model |
| `internship_job.py` | Job description model |
| `config.py` | Configuration & settings |

## 🤔 FAQ

**Q: Do I need an OpenAI API key?**
A: No! Uses mock LLM by default. Works offline. Upgrade later if needed.

**Q: Can I integrate my own LLM?**
A: Yes! Edit `_call_llm()` in `ai_agent.py` to use your LLM.

**Q: How do I add more students/jobs?**
A: Create JSON files in `example_data/` and load them via CLI.

**Q: Can I deploy this?**
A: Yes! The Flask API is production-ready (add authentication first).

---

## 🎯 Next Steps

1. **Try the CLI**: `python cli.py`
2. **Load examples**: Option 5 in CLI menu
3. **Test the API**: `python app.py`
4. **Read the code**: `ai_agent.py` is the core
5. **Customize prompts**: Edit prompt templates in `ai_agent.py`

---

**Questions? Check README.md for detailed docs!**
