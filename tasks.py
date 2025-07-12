# tasks.py
from crewai import Agent, Task # <-- THE FIX FOR THE NameError
from models import DynamicExtractionResult

def create_dynamic_extraction_task(agent: Agent) -> Task:
    """Defines the dynamic entity extraction task."""
    return Task(
        description=(
            "Analyze the provided DOCUMENT TEXT and identify all important entities. "
            "Structure your findings as a JSON object where keys are the labels from the document "
            "and values are the corresponding data. For example: '{\"Loan Amount\": 162000.0, \"Interest Rate\": 3.875, \"Lender\": \"Ficus Bank\"}'.\n"
            "--- DOCUMENT TEXT ---\n"
            "{invoice_text}\n"
            "--- END DOCUMENT TEXT ---"
        ),
        expected_output="A single JSON object representing the dynamically identified key-value pairs.",
        agent=agent
    )

def create_validation_task(agent: Agent, context_task: Task) -> Task:
    """Defines the validation task, which enforces a final structured output."""
    return Task(
        description=(
            "You have been given raw text and a JSON object of extracted entities from a previous step. "
            "Your critical task is to validate this JSON against the raw text. "
            "1. For each key-value pair, confirm its accuracy with the raw text. Correct any errors. "
            "2. Scan the raw text for any important information the first agent may have missed and add it to the dictionary. "
            "3. Provide a summary of your findings in the 'review_summary'.\n\n"
            "--- ORIGINAL DOCUMENT TEXT ---\n"
            "{invoice_text}"
        ),
        expected_output=(
            "A final JSON object strictly adhering to the 'DynamicExtractionResult' schema, "
            "containing your review summary and the final, validated key-value dictionary."
        ),
        agent=agent,
        context=[context_task],
        output_pydantic=DynamicExtractionResult
    )