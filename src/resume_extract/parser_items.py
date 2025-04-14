from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class PersonalDetails(BaseModel):
    name: Optional[str] = Field(
        None, description="Full name of the candidate."
    )
    email: Optional[EmailStr] = Field(
        None, description="Candidate's primary email address."
    )
    mobile: Optional[str] = Field(
        None, description="Candidate's mobile phone number including country code if applicable."
    )

from pydantic import BaseModel, Field
from typing import List, Optional

class Project(BaseModel):
    title: Optional[str] = Field(
        None, description="Title or name of the project."
    )
    description: Optional[str] = Field(
        None, description="Short overview or summary of the project."
    )
    technologies: List[str] = Field(
        default_factory=list, description="List of technologies or tools used in the project."
    )


from pydantic import BaseModel, Field
from typing import Optional

class WorkExperience(BaseModel):
    company: Optional[str] = Field(
        None, description="Name of the company where the candidate worked."
    )
    title: Optional[str] = Field(
        None, description="Job title held at the company."
    )
    duration: Optional[str] = Field(
        None, description="Employment period (e.g., 'Jan 2018 - Dec 2020')."
    )
    responsibilities: Optional[str] = Field(
        None, description="Brief description of the candidate's responsibilities or achievements in the role."
    )
    projects: List[Project] = Field(
            default_factory=list, description="A list of projects the candidate has worked on" 
    )


from pydantic import BaseModel, Field
from typing import List

class Skills(BaseModel):
    skills: List[str] = Field(
        default_factory=list, description="List of the candidate's technical and soft skills."
    )

from pydantic import BaseModel, Field
from typing import Optional

class Education(BaseModel):
    institution: Optional[str] = Field(
        None, description="Name of the educational institution."
    )
    degree: Optional[str] = Field(
        None, description="Degree or certification earned by the candidate."
    )
    year: Optional[str] = Field(
        None, description="Time period of attendance or graduation year."
    )

class ResumeSkills(BaseModel):
    technical_skills: List[str]
    soft_skills: List[str]
    domain_specific_skills: List[str]
    tools_and_platforms: List[str]
    languages: List[str]

from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class Publication(BaseModel):
    title: str
    authors: List[str]
    publication_venue: Optional[str] = None
    year: Optional[int] = None
    doi_or_link: Optional[HttpUrl] = None
    description: Optional[str] = None

