from pydantic import BaseModel, Field
from typing import Dict, Literal

class BaseExtractionSchema(BaseModel):
    reasoning: str = Field(
        description="Think step-by-step about the transcript before extracting data."
    )

    class LayoutConfig:
        # Options: "UNIQUE" (one-to-one) or "TABLE_FLATTEN" (lists into one box)
        layout_type: Literal["UNIQUE", "TABLE_FLATTEN"]
        # Maps a List field name to a single PDF box name
        table_mapping: Dict[str, str] = {}
        list_formatting: str | None = None