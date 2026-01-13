"""
Student Profile Data Model
"""
from typing import List, Dict
from dataclasses import dataclass, asdict
import json


@dataclass
class StudentProfile:
    """Represents a student's profile with skills and interests"""
    name: str
    email: str
    skills: List[str]  # e.g., ["Python", "JavaScript", "React"]
    interests: List[str]  # e.g., ["Web Development", "AI/ML"]
    experience: str  # Brief description of past experience
    cgpa: float  # Cumulative GPA (0-4.0)
    resume_text: str = ""  # Optional: existing resume text
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StudentProfile':
        """Create from dictionary"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'StudentProfile':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def get_profile_summary(self) -> str:
        """Get a formatted summary of the profile"""
        return f"""
Student Profile: {self.name}
Email: {self.email}
CGPA: {self.cgpa}/4.0
Skills: {', '.join(self.skills)}
Interests: {', '.join(self.interests)}
Experience: {self.experience}
"""
