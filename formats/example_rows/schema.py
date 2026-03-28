from pydantic import Field, BaseModel
from typing import List
from base_schema import BaseExtractionSchema

class Medication(BaseModel):
    name: str = Field(description="Name of drug")
    dose: str = Field(description="Dosage of drug")
    freq: str = Field(description="How often and how long to take drug")

class ReportSchema(BaseExtractionSchema):
    patient_name: str = Field(description="Name of patient")
    # The LLM extracts this as a clean list of objects
    medications: List[Medication] = Field(description="List of meds.")

    class LayoutConfig:
        layout_type = "TABLE_FLATTEN"
        # "Take the 'medications' list and squash it into the 'medication' in the PDF"
        table_mapping = {"medications": "medication"}
        list_formatting = {
        "medications": "{name} | {dose} ({freq})"
    }