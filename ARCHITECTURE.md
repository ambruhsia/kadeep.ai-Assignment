# InternHub - Architecture & Design Document

## 🏗️ System Architecture

### High-Level Overview
```
┌──────────────────────────────────────────────────────┐
│                    InternHub System                   │
├──────────────────────────────────────────────────────┤
│                                                      │
│   User Interface Layer                               │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│   │     CLI      │  │  Flask API   │  │   JSON   │ │
│   │   (cli.py)   │  │  (app.py)    │  │  Files   │ │
│   └──────────────┘  └──────────────┘  └──────────┘ │
│         │                  │                 │      │
│         └──────────────────┼─────────────────┘      │
│                            ▼                        │
│   Data Models Layer (Serialization)                 │
│   ┌──────────────┐      ┌──────────────┐           │
│   │  Student     │      │ Internship   │           │
│   │  Profile     │      │    Job       │           │
│   │ (JSON/Dict)  │      │  (JSON/Dict) │           │
│   └──────────────┘      └──────────────┘           │
│         │                      │                    │
│         └──────────────┬───────┘                    │
│                        ▼                            │
│   Core AI Engine Layer                              │
│   ┌────────────────────────────────────────────┐   │
│   │      InternHubAIAgent (ai_agent.py)        │   │
│   ├────────────────────────────────────────────┤   │
│   │  - analyze_match()                         │   │
│   │  - generate_optimized_resume()             │   │
│   │  - calculate_ats_score()                   │   │
│   │  - _calculate_match_score()                │   │
│   │  - _analyze_skill_gaps()                   │   │
│   │  - _generate_recommendation()              │   │
│   └────────────────────────────────────────────┘   │
│         │         │         │         │            │
│    ┌────▼──┐  ┌───▼─┐  ┌────▼──┐  ┌─▼──┐          │
│    │Scoring│  │Gaps │  │Resume │  │ATS │          │
│    │Algo   │  │Analysis│  Gen   │  │Score         │
│    └───────┘  └──────┘  └───────┘  └─────┘        │
│         │                            │             │
│         └────────────────┬───────────┘             │
│                          ▼                         │
│   LLM Layer (Abstract)                             │
│   ┌────────────────────────────────────────────┐   │
│   │  _call_llm() Router                        │   │
│   │  ├─ Real: OpenAI API                       │   │
│   │  └─ Mock: Template-based fallback          │   │
│   └────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 📊 Core Algorithm Details

### 1. Match Scoring Algorithm

**Formula**:
```
Match_Score = (Required_Skills_Coverage × 0.6) 
            + (Preferred_Skills_Coverage × 0.3)
            + (Interest_Alignment × 0.2)
            + (CGPA_Factor × 0.1)
```

**Components**:

#### Required Skills Coverage (60% weight)
```python
required_skill_matches = count(skill ∈ required_skills 
                               where student_has_skill(skill))
required_coverage = required_skill_matches / len(required_skills)
score_component = required_coverage × 0.6
```

**Rationale**: Required skills are critical for job success. Highest weight.

#### Preferred Skills Coverage (30% weight)
```python
preferred_skill_matches = count(skill ∈ preferred_skills 
                                where student_has_skill(skill))
preferred_coverage = preferred_skill_matches / len(preferred_skills)
score_component = preferred_coverage × 0.3
```

**Rationale**: Nice-to-have skills show initiative and extra effort.

#### Interest Alignment (20% weight)
```python
interest_match = any(student_interest.lower() in job_description.lower())
score_component = 0.2 if interest_match else 0.0
```

**Rationale**: Passion and genuine interest correlate with performance.

#### CGPA Factor (10% weight)
```python
cgpa_score = min(student_cgpa / 4.0, 1.0) × 0.1
```

**Rationale**: Academic performance is an indicator of learning ability.

**Threshold Logic**:
- Score ≥ 0.5: "Strong fit" - Recommend applying
- Score 0.3-0.5: "Decent fit" - Suggest upskilling
- Score < 0.3: "Challenge fit" - Requires preparation

### 2. Skill Gap Analysis

**Algorithm**:
```python
for each required_skill in job.required_skills:
    if skill_not_in_student_skills(required_skill):
        gap = {
            skill: required_skill,
            category: categorize_skill(required_skill),
            importance: "Required"
        }
        gaps.append(gap)

# Limit to MAX_SKILL_GAPS for actionability
return gaps[:MAX_SKILL_GAPS]
```

**Skill Categorization**:
- **Programming Language**: Python, JavaScript, Java, C++, Go, Rust
- **Framework/Library**: React, Django, Flask, Spring, Vue, Angular
- **Cloud Platform**: AWS, Azure, GCP
- **Technical Skill**: Other domain-specific skills

**Benefit**: Provides actionable learning roadmap for students.

### 3. Resume Generation via Prompts

**Prompt Engineering Strategy**:

```python
prompt = f"""You are a resume optimization expert.

Student Profile:
- Skills: {skills}
- Experience: {experience}
- CGPA: {cgpa}

Target Job:
- Title: {title}
- Required: {required_skills}
- Key Responsibilities: {responsibilities[:3]}

Task: Generate a tailored, ATS-friendly resume.
Focus on: {required_skills[:3]}
Length: ~300 words, professional format.

Resume:"""
```

**Key Techniques**:
1. **Role Definition**: "You are a resume optimization expert"
2. **Context Injection**: Provide both student and job info
3. **Clear Instructions**: Specify focus skills and constraints
4. **Format Hints**: ATS-friendly, professional, concise

**LLM Fallback (Mock)**:
```
If prompt contains "resume":
  Return professional resume template
  - Professional summary
  - Technical skills (aligned with job)
  - Experience highlights
  - Education
```

### 4. ATS Score Calculation

**Algorithm**:
```python
all_keywords = set(required_skills + preferred_skills)
matched_keywords = set()

for keyword in all_keywords:
    if keyword.lower() in resume_text.lower():
        matched_keywords.add(keyword)

ats_score = len(matched_keywords) / len(all_keywords)
```

**Scoring**:
- **80-100%**: Excellent - Likely to pass ATS
- **60-79%**: Good - Should be fine
- **40-59%**: Fair - May be filtered
- **<40%**: Poor - High risk of filtering

**Importance**: ATS systems eliminate ~75% of applications before human review.

## 🔄 Data Flow

### Scenario: Complete Analysis

```
User Input
    ↓
┌───────────────────────────────────────┐
│  CLI/API Request                      │
│  ├─ Student Profile (JSON/Dict)       │
│  └─ Job Description (JSON/Dict)       │
└───────────────────────────────────────┘
    ↓
Deserialize → StudentProfile + InternshipJob objects
    ↓
┌───────────────────────────────────────────────────┐
│ InternHubAIAgent.analyze_match()                 │
│ ├─ _calculate_match_score() → 0.78              │
│ ├─ _analyze_skill_gaps() → [Gap, Gap]            │
│ ├─ _identify_strengths() → [Str1, Str2]          │
│ └─ _generate_recommendation() → "Apply now..."   │
└───────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────┐
│ InternHubAIAgent.generate_optimized_resume()    │
│ └─ _call_llm(prompt) → Resume text              │
└───────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────┐
│ InternHubAIAgent.calculate_ats_score()           │
│ └─ Keyword matching → 0.80 (80%)                │
└───────────────────────────────────────────────────┘
    ↓
Return combined results
    ↓
Format & Display to user
```

## 🧠 Prompt Design Patterns

### Pattern 1: Role-Based Prompts
```python
prompt = f"You are a {role}. {task}"
# Example: "You are a resume expert. Optimize this..."
```

### Pattern 2: Context Injection
```python
prompt = f"""Context:
{student_info}
{job_info}

Task: {specific_task}"""
```

### Pattern 3: Output Format Specification
```python
prompt = f"...Output format: {format_specification}..."
# Example: "Output as JSON", "Keep under 300 words"
```

### Pattern 4: Conditional Logic
```python
if confidence_score > 0.7:
    prompt += "This is a strong match. Be encouraging."
else:
    prompt += "This role is challenging. Be realistic."
```

## 🔌 LLM Integration

### Real LLM (OpenAI)
```python
if USE_MOCK_LLM == False:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content
```

### Mock LLM (Fallback)
```python
if USE_MOCK_LLM == True:
    # Pattern matching on prompt intent
    if "resume" in prompt.lower():
        return professional_resume_template()
    elif "recommendation" in prompt.lower():
        return contextualized_recommendation(match_score)
```

**Benefit**: Works offline, no API costs, fast prototyping.

## 📈 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Mock LLM Default** | Works offline, fast testing, no API costs |
| **Modular Components** | Easy to test, update, or replace |
| **JSON Serialization** | Easy to store, transmit, integrate with other systems |
| **Threshold-based Scoring** | Clear, interpretable decisions for users |
| **Prompt-based Generation** | LLM-agnostic, easy to customize, educational |
| **CLI + API** | Both for testing and production use |

## 🧪 Testing Strategy

### Unit Tests (Implicit)
- Match score calculation
- Skill gap identification
- Keyword matching (ATS)
- JSON serialization/deserialization

### Integration Tests
- Full pipeline (profile → analysis)
- LLM fallback mechanism
- API endpoints

### Manual Tests (Included)
- `test_internhub.py`: 6 comprehensive test cases
- CLI quick test mode
- Example JSON loading

## 🚀 Scalability Considerations

### Current (MVP)
- In-memory data only
- Single request handling
- Mock LLM

### Future Enhancements
```
Database Layer
│
├─ Student profiles
├─ Job postings
├─ Application tracking
└─ Analytics

Batch Processing
│
├─ Process 100s of candidates
├─ Scheduled analysis
└─ Bulk resume generation

Caching
│
├─ Cache LLM responses
├─ Cache skill categorizations
└─ Cache common analyses

Async Processing
│
├─ Queue-based job processing
├─ Background resume generation
└─ Email notifications
```

## 🔐 Security Considerations

**Current (MVP)**:
- No authentication (demo only)
- No data persistence
- No sensitive data

**Production Additions**:
```python
# Authentication
from flask_jwt_extended import JWTManager

# Data encryption
from cryptography.fernet import Fernet

# Rate limiting
from flask_limiter import Limiter

# Input validation
from marshmallow import Schema, validate
```

## 📊 Performance Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Match analysis | <100ms | <50ms |
| Resume generation | ~300ms (LLM) | <500ms |
| ATS calculation | <10ms | <5ms |
| Full pipeline | ~400ms | <600ms |

**Note**: Mock LLM is ~10-50ms, Real LLM is 1-3s depending on API.

---

## 🎯 Core Concepts Summary

### Explainability
All scores have clear calculation logic - not black boxes.

### Modularity
Each component (scoring, gaps, resume, ATS) is independent.

### Extensibility
Easy to add new features or swap components.

### Simplicity
No complex ML models - just intelligent logic and prompts.

### LLM-Agnostic
Works with any LLM through simple interface.

---

**InternHub: Intelligent internship matching through prompt engineering and algorithmic reasoning.**
