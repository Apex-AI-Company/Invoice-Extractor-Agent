# models.py
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class DynamicExtractionResult(BaseModel):
    """The final, validated data model produced by the Validator Agent."""
    review_summary: str = Field(description="A summary of the review, noting any corrections, additions, or reasons for concern.")
    extracted_entities: Dict[str, Optional[Any]] = Field(description="The final, validated dictionary of key-value pairs extracted from the document.")