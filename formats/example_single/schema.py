from pydantic import Field
from base_schema import BaseExtractionSchema

class ReportSchema(BaseExtractionSchema):
    patient_name: str = Field(description="Full name")
    symptoms: str = Field(description="Summary of issues")

    class LayoutConfig:
        layout_type = "UNIQUE"
        # "Take the 'medications' list and squash it into the 'medication' in the PDF"
        table_mapping = {"medications": "medication"}