from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Stage 1 & 2: Classification and Validation ---
class ClassificationResult(BaseModel):
    """Data model for the output of the classification and validation agents."""
    document_type: str = Field(description="The identified type of the document (e.g., 'Invoice', 'Loan Disclosure', 'Resume', 'Unknown').")
    confidence_score: float = Field(description="A confidence score (0.0 to 1.0) for the classification.")
    reasoning: str = Field(description="A brief explanation for the classification decision.")

# --- Stage 3: Extraction ---
class LineItem(BaseModel):
    """Data model for a single line item on an invoice or statement."""
    description: Optional[str] = Field(description="The description of the product, service, or charge.")
    quantity: Optional[float] = Field(description="The quantity of the item, if applicable.")
    unit_price: Optional[float] = Field(description="The price of a single unit of the item, if applicable.")
    total_price: Optional[float] = Field(description="The total price for this line item.")

class InvoiceData(BaseModel):
    """The main data model for extracting structured data from a financial document."""
    vendor_name: Optional[str] = Field(description="The name of the company or vendor issuing the document.")
    buyer_name: Optional[str] = Field(description="The name of the person or company receiving the document.")
    invoice_number: Optional[str] = Field(description="The unique identifier for the document.")
    invoice_date: Optional[str] = Field(description="The date the document was issued.")
    total_due: Optional[float] = Field(description="The final, total amount due or the primary amount of the document (e.g., Loan Amount).")
    line_items: List[LineItem] = Field(description="A list of all detailed line items.", default=[])

# --- Stage 4 & 5: Review and Final Consolidation ---
class FinalReport(BaseModel):
    """The final, consolidated report containing all processed information."""
    final_document_type: str = Field(description="The validated type of the document.")
    extraction_summary: str = Field(description="A brief, human-readable summary of the key extracted information.")
    is_flagged_by_reviewer: bool = Field(description="Was the document flagged for inconsistencies by the Reviewer Agent?")
    reviewer_comments: str = Field(description="All comments and corrections made by the Reviewer Agent.")
    structured_data: Dict[str, Any] = Field(description="The final, validated dictionary of all key-value pairs extracted from the document.")