"""
InternHub AI Agent - Core Matching & Analysis Engine
Handles: Match scoring, Skill gap analysis, Resume generation, ATS scoring
"""
import re
import json
from typing import Dict, List, Tuple
from student_profile import StudentProfile
from internship_job import InternshipJob
import config


class InternHubAIAgent:
    """AI Agent for internship matching and analysis"""
    
    def __init__(self, use_mock: bool = True):
        """Initialize the AI agent"""
        self.use_mock = use_mock
        if not use_mock and config.OPENAI_API_KEY:
            try:
                import openai
                openai.api_key = config.OPENAI_API_KEY
                self.openai = openai
            except ImportError:
                print("Warning: OpenAI module not installed. Falling back to mock LLM.")
                self.use_mock = True
    
    def analyze_match(
        self, 
        student: StudentProfile, 
        job: InternshipJob
    ) -> Dict:
        """
        Analyze how well a student matches an internship
        Returns: match_score, skill_gaps, strengths, recommendation
        """
        # 1. Calculate match confidence score
        confidence = self._calculate_match_score(student, job)
        
        # 2. Identify skill gaps
        skill_gaps = self._analyze_skill_gaps(student, job)
        
        # 3. Identify student strengths
        strengths = self._identify_strengths(student, job)
        
        # 4. Generate recommendation
        recommendation = self._generate_recommendation(
            student, job, confidence, skill_gaps
        )
        
        return {
            "confidence_score": round(confidence, 2),
            "match_percentage": f"{int(confidence * 100)}%",
            "skill_gaps": skill_gaps,
            "strengths": strengths,
            "recommendation": recommendation,
            "is_match": confidence >= config.CONFIDENCE_THRESHOLD
        }
    
    def generate_optimized_resume(
        self,
        student: StudentProfile,
        job: InternshipJob
    ) -> str:
        """
        Generate a resume optimized for the JD using prompt engineering
        Focuses on relevant skills, reframes experience
        """
        prompt = f"""You are a resume optimization expert. 
        
Student Profile:
- Name: {student.name}
- Skills: {', '.join(student.skills)}
- Interests: {', '.join(student.interests)}
- Experience: {student.experience}
- CGPA: {student.cgpa}

Job Description:
- Title: {job.title}
- Company: {job.company}
- Required Skills: {', '.join(job.required_skills)}
- Preferred Skills: {', '.join(job.preferred_skills)}
- Key Responsibilities: {', '.join(job.responsibilities[:3])}

Task: Generate a concise, ATS-friendly resume tailored to this internship. 
Focus on highlighting relevant skills and experiences. 
Format as a professional resume snippet (under 300 words).
Emphasize alignment with: {', '.join(job.required_skills[:3])}

Resume:"""
        
        return self._call_llm(prompt)
    
    def calculate_ats_score(
        self,
        student: StudentProfile,
        job: InternshipJob,
        resume_text: str = None
    ) -> Dict:
        """
        Calculate ATS (Applicant Tracking System) score
        Checks keyword matches, formatting, relevance
        """
        resume = resume_text or student.resume_text or ""
        
        # Simple keyword matching for ATS
        all_keywords = set(job.required_skills + job.preferred_skills)
        matched_keywords = set()
        
        for keyword in all_keywords:
            if keyword.lower() in resume.lower():
                matched_keywords.add(keyword)
        
        # ATS score: keyword match percentage
        ats_score = len(matched_keywords) / len(all_keywords) if all_keywords else 0
        
        return {
            "ats_score": round(ats_score, 2),
            "ats_percentage": f"{int(ats_score * 100)}%",
            "matched_keywords": list(matched_keywords),
            "missing_keywords": list(all_keywords - matched_keywords),
            "keyword_count": len(all_keywords),
            "matched_count": len(matched_keywords)
        }
    
    # ==================== PRIVATE METHODS ====================
    
    def _calculate_match_score(
        self, 
        student: StudentProfile, 
        job: InternshipJob
    ) -> float:
        """
        Calculate match confidence score (0-1)
        Considers skill overlap, interest alignment, and CGPA
        """
        # Skill matching
        student_skills_lower = [s.lower() for s in student.skills]
        required_skill_matches = sum(
            1 for req in job.required_skills 
            if any(req.lower() in s for s in student_skills_lower)
        )
        preferred_skill_matches = sum(
            1 for pref in job.preferred_skills 
            if any(pref.lower() in s for s in student_skills_lower)
        )
        
        # Score components
        skill_coverage = (
            required_skill_matches / len(job.required_skills) * 0.6 +
            preferred_skill_matches / len(job.preferred_skills) * 0.3
        ) if job.required_skills else 0
        
        # Interest alignment
        interest_match = any(
            interest.lower() in ' '.join(job.description).lower()
            for interest in student.interests
        )
        interest_score = 0.2 if interest_match else 0
        
        # CGPA factor (3.0+ is good)
        cgpa_score = min(student.cgpa / 4.0, 1.0) * 0.1
        
        total_score = min(skill_coverage + interest_score + cgpa_score, 1.0)
        return total_score
    
    def _analyze_skill_gaps(
        self,
        student: StudentProfile,
        job: InternshipJob
    ) -> List[Dict]:
        """Identify skill gaps between student and job requirements"""
        student_skills_lower = [s.lower() for s in student.skills]
        gaps = []
        
        for req_skill in job.required_skills[:config.MAX_SKILL_GAPS]:
            has_skill = any(req_skill.lower() in s for s in student_skills_lower)
            if not has_skill:
                gaps.append({
                    "skill": req_skill,
                    "category": self._categorize_skill(req_skill),
                    "importance": "Required"
                })
        
        return gaps
    
    def _identify_strengths(
        self,
        student: StudentProfile,
        job: InternshipJob
    ) -> List[str]:
        """Identify matching strengths"""
        student_skills_lower = [s.lower() for s in student.skills]
        strengths = []
        
        for req_skill in job.required_skills[:3]:
            for student_skill in student.skills:
                if req_skill.lower() in student_skill.lower():
                    strengths.append(f"Strong in {student_skill} (aligns with {req_skill})")
        
        if student.cgpa >= 3.5:
            strengths.append("Excellent academic performance (CGPA ≥ 3.5)")
        
        return strengths if strengths else ["Motivated candidate with relevant interests"]
    
    def _generate_recommendation(
        self,
        student: StudentProfile,
        job: InternshipJob,
        confidence: float,
        skill_gaps: List[Dict]
    ) -> str:
        """Generate personalized recommendation using prompt engineering"""
        
        prompt = f"""You are a career advisor for an internship platform.
        
Student: {student.name}
Match Confidence: {confidence * 100:.0f}%
Student Skills: {', '.join(student.skills)}
Student Interests: {', '.join(student.interests)}

Job: {job.title} at {job.company}
Required: {', '.join(job.required_skills)}
Skill Gaps: {', '.join(gap['skill'] for gap in skill_gaps)}

Provide a 2-3 sentence personalized recommendation on whether this student should apply.
Consider the match score and skill gaps. Be encouraging but honest.

Recommendation:"""
        
        return self._call_llm(prompt)
    
    def _categorize_skill(self, skill: str) -> str:
        """Categorize a skill (Programming, Tools, Domain, etc.)"""
        programming_langs = ["python", "javascript", "java", "c++", "go", "rust"]
        frameworks = ["react", "django", "flask", "spring", "vue", "angular"]
        cloud = ["aws", "azure", "gcp", "google cloud"]
        
        skill_lower = skill.lower()
        
        if any(lang in skill_lower for lang in programming_langs):
            return "Programming Language"
        elif any(fw in skill_lower for fw in frameworks):
            return "Framework/Library"
        elif any(c in skill_lower for c in cloud):
            return "Cloud Platform"
        else:
            return "Technical Skill"
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call LLM (real or mock) to generate text
        Supports OpenAI API or falls back to mock responses
        """
        if self.use_mock:
            return self._mock_llm_response(prompt)
        else:
            return self._call_openai(prompt)
    
    def _mock_llm_response(self, prompt: str) -> str:
        """Generate mock LLM response based on prompt intent"""
        
        if "resume" in prompt.lower():
            return """
PROFESSIONAL SUMMARY
Passionate developer with strong skills in Python and JavaScript, seeking to apply technical expertise and problem-solving abilities in a dynamic internship role.

TECHNICAL SKILLS
- Languages: Python, JavaScript
- Technologies: REST APIs, Database Design
- Tools: Git, Linux

EXPERIENCE HIGHLIGHTS
- Developed multiple projects using modern frameworks
- Strong foundation in computer science fundamentals
- Quick learner with enthusiasm for new technologies

EDUCATION
Currently pursuing studies with focus on software development and computer science.
"""
        
        elif "recommendation" in prompt.lower():
            if "80" in prompt or "90" in prompt:
                return "This student is an excellent fit for the role. Their skill set strongly aligns with the position requirements, and their demonstrated interests suggest genuine passion for the work. We recommend moving forward with the application immediately."
            elif "50" in prompt or "60" in prompt:
                return "This student shows promise and has some relevant experience. While there are skill gaps, their foundational knowledge and interests suggest they could grow into the role with some preparation. We recommend applying and highlighting transferable skills."
            else:
                return "While this role might be challenging given the skill gaps, the student's motivation and related interests could make them a valuable long-term fit. Consider applying and addressing skill gaps in the cover letter."
        
        return "Generated response based on the provided context and job description."
    
    def _call_openai(self, prompt: str) -> str:
        """Call real OpenAI API"""
        try:
            response = self.openai.ChatCompletion.create(
                model=config.MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return self._mock_llm_response(prompt)


# Convenience functions
def analyze_internship_fit(
    student: StudentProfile,
    job: InternshipJob,
    use_mock: bool = True
) -> Dict:
    """Analyze internship fit for a student"""
    agent = InternHubAIAgent(use_mock=use_mock)
    return agent.analyze_match(student, job)


def generate_resume(
    student: StudentProfile,
    job: InternshipJob,
    use_mock: bool = True
) -> str:
    """Generate optimized resume"""
    agent = InternHubAIAgent(use_mock=use_mock)
    return agent.generate_optimized_resume(student, job)


def get_ats_score(
    student: StudentProfile,
    job: InternshipJob,
    resume_text: str = None,
    use_mock: bool = True
) -> Dict:
    """Get ATS score"""
    agent = InternHubAIAgent(use_mock=use_mock)
    return agent.calculate_ats_score(student, job, resume_text)
