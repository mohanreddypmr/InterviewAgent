from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    question: str = Field(..., description="The actual interview question")
    category: str = Field(..., description="Category of the question (e.g., technical, behavioral)")
    difficulty: str = Field(..., description="Difficulty level (easy, medium, hard)")
    context: Optional[str] = Field(None, description="Additional context or explanation for the question")
    expected_answer_points: Optional[List[str]] = Field(default_factory=list, description="Key points expected in the answer")

class SectionQuestions(BaseModel):
    section_name: str = Field(..., description="Name of the resume section (e.g., work_experience, projects)")
    section_title: str = Field(..., description="Specific title within the section (e.g., company name, project name)")
    questions: List[Question] = Field(..., description="List of questions for this section")

class GeneratedQuestions(BaseModel):
    total_questions: int = Field(..., description="Total number of questions generated")
    sections: List[SectionQuestions] = Field(..., description="List of questions organized by section") 

class ListQuestion(BaseModel):
    questions: List[Question] = Field(..., description="List of questions")