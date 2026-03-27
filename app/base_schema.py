from pydantic import BaseModel, Field

class BaseExtractionSchema(BaseModel):
    reasoning: str = Field(
        description="Think step-by-step about the transcript. Briefly explain your logic for what information you are extracting and what information you are explicitly ignoring, before you fill out the rest of the fields."
    )