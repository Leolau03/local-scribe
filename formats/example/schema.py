from pydantic import Field
from base_schema import BaseExtractionSchema

class ReportSchema(BaseExtractionSchema):
    patient_name: str = Field(description="Full name")
    symptoms: str = Field(description="Summary of issues")