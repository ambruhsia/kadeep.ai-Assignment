"""
Internship Job Description Data Model
"""
from typing import List, Dict
from dataclasses import dataclass, asdict
import json


@dataclass
class InternshipJob:
    """Represents an internship job description"""
    title: str
    company: str
    description: str  # Full JD text
    required_skills: List[str]  # e.g., ["Python", "REST APIs"]
    preferred_skills: List[str]  # e.g., ["Docker", "AWS"]
    responsibilities: List[str]  # Job responsibilities
    duration_months: int  # Duration in months
    location: str  # Location (e.g., "Remote", "San Francisco")
    compensation: str = "Competitive"  # Stipend/salary info
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'InternshipJob':
        """Create from dictionary"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'InternshipJob':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def get_jd_summary(self) -> str:
        """Get a formatted summary of the JD"""
        return f"""
Job: {self.title}
Company: {self.company}
Location: {self.location}
Duration: {self.duration_months} months
Compensation: {self.compensation}

Required Skills: {', '.join(self.required_skills)}
Preferred Skills: {', '.join(self.preferred_skills)}

Responsibilities:
{chr(10).join(f'  - {r}' for r in self.responsibilities)}

Full Description:
{self.description}
"""
