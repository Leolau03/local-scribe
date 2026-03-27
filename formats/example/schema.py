from pydantic import BaseModel, Field
class ReportSchema(BaseModel):
    patient_name: str = Field(description="Full name")
    symptoms: str = Field(description="Summary of issues")