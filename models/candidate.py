from typing import Optional, List
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    """Personal information of the candidate"""
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    level: Optional[str] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    years_of_experience: Optional[str] = None
    desired_work_locations: Optional[List[str]] = Field(default_factory=list)
    job_rank: Optional[str] = None


class ContactInfo(BaseModel):
    """Contact information"""
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class Skill(BaseModel):
    """Skill with proficiency level"""
    name: str
    proficiency: Optional[str] = None
    category: Optional[str] = None


class Language(BaseModel):
    """Language proficiency"""
    language: str
    proficiency: Optional[str] = None


class Education(BaseModel):
    """Education background"""
    institution_name: Optional[str] = None
    degree: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[str] = None
    duration: Optional[str] = None


class Project(BaseModel):
    """Project experience"""
    project_name: Optional[str] = None
    description: Optional[str] = None
    time: Optional[str] = None


class Achievement(BaseModel):
    """Achievements and certifications"""
    title: str
    description: Optional[str] = None
    date: Optional[str] = None


class HRFields(BaseModel):
    """HR and extension fields"""
    hiring_type: Optional[str] = None
    is_terminal: Optional[bool] = None
    can_rehire: Optional[bool] = None
    is_fsofter: Optional[bool] = None
    is_utilization: Optional[bool] = None


class Candidate(BaseModel):
    """
    Represents the complete CV data structure of a candidate
    """
    # Core sections
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    
    # Skills and languages
    skills: List[Skill] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    
    # Education and experience
    education: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    achievements: List[Achievement] = Field(default_factory=list)
    
    # HR fields
    hr_fields: HRFields = Field(default_factory=HRFields)
    
    # AI Analysis fields (populated after AI processing)
    ai_matched_role: Optional[str] = None
    ai_confidence_score: Optional[float] = None
    ai_jd_match_score: Optional[float] = None
    ai_extracted_summary: Optional[str] = None
