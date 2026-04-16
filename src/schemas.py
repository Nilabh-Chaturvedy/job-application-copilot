from pydantic import BaseModel
from typing import List
class plan(BaseModel):

    steps : List[str]


class ExperienceItem(BaseModel):
    company : str
    role : str
    location : str
    dates : str
    bullets : List[str]

class EducationItem(BaseModel):
    institution : str
    degree: str
    dates: str

class StructuredResume(BaseModel):
    summary :str
    experience : List[ExperienceItem]
    skills : List[str]
    education : List[EducationItem]
