from langchain_core.pydantic_v1 import BaseModel, Field

class ToCurrikiLibraryExplorer(BaseModel):
    """Transfer work to a spacialized agent to handle the exploration of the Curriki Library."""    
    request: str = Field(description="Messages or requests from the user in order to find any information or knowledge in the Curriki Library.")