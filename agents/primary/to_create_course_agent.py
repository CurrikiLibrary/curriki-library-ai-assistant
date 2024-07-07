from langchain_core.pydantic_v1 import BaseModel, Field

class ToCreateCourseAgent(BaseModel):
    """Transfer work to a spacialized agent to handle the creation of a course."""
    request: str = Field(description="Messages or requests from the user in order to create a course.")
    title: str = Field(description="The title of the course.")
    description: str = Field(description="The description of the course.")
    subject: str = Field(description="The subject of the course.")
    grade_level: str = Field(description="The grade level of the course.")
    keywords: str = Field(description="The keywords of the course.")

    class Config:
        schema_extra = {
            "example": {
                "request": "I want to create a course.",
                "title": "Mathematics",
                "description": "This course is about mathematics.",
                "subject": "Mathematics",
                "grade_level": "Grade 1",
                "keywords": "mathematics, grade 1"
            },
            "example 2": {
                "request": "Create a course.",
                "title": "Science",
                "description": "This course is about science.",
                "subject": "Science",
                "grade_level": "Grade 2",
                "keywords": "science, grade 2"
            }
        }
    