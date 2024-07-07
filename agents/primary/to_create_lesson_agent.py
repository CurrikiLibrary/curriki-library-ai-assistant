from langchain_core.pydantic_v1 import BaseModel, Field

class ToCreateLessonAgent(BaseModel):
    """Transfer work to a spacialized agent to handle the creation of a lesson for course."""
    request: str = Field(description="Messages or requests from the user in order to create a lesson.")
    title: str = Field(description="The title of the lesson.")
    description: str = Field(description="The description of the lesson.")
    type: str = Field(description="The type of the lesson.")
    course_identifier: str = Field(description="The identifier of the course.")

    class Config:
        schema_extra = {
            "example": {
                "request": "I want to create a lesson.",
                "title": "Lesson 1",
                "description": "This lesson is about mathematics.",
                "type": "Lesson",
                "course_identifier": "1"
            },
            "example 2": {
                "request": "Create a lesson.",
                "title": "Lesson 2",
                "description": "This lesson is about science.",
                "type": "Lesson",
                "course_identifier": "1"
            }
        }
    