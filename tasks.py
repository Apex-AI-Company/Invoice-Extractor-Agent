from crewai import Agent, Task
from models import ClassificationResult, InvoiceData, FinalReport

def create_classification_task(agent: Agent) -> Task:
    """
    Analyzes the beginning of the text to make a quick classification.
    """
    return Task(
        description=(
            "Analyze the first 500 characters of the DOCUMENT TEXT to determine its type from the list: "
            "['Invoice', 'Loan Disclosure', 'Resume', 'Unknown'].\n"
            "--- DOCUMENT TEXT ---\n{invoice_text}"
        ),
        expected_output="A JSON object conforming to the 'ClassificationResult' schema.",
        agent=agent,
        output_pydantic=ClassificationResult
    )

def create_validation_task(agent: Agent, context_task: Task) -> Task:
    """
    Validates the initial classification using the full text.
    The output of the previous task is automatically available in the context.
    """
    return Task(
        description=(
            "Review the initial classification against the full DOCUMENT TEXT. "
            "Confirm or correct the 'document_type' based on all available information.\n"
            "--- DOCUMENT TEXT ---\n{invoice_text}"
        ),
        expected_output="A JSON object conforming to the 'ClassificationResult' schema with the validated type.",
        agent=agent,
        context=[context_task],
        output_pydantic=ClassificationResult
    )

def create_extraction_task(agent: Agent, context_task: Task) -> Task:
    """
    Extracts data. The validated document type from the previous task is passed in the context.
    We re-provide the full text to ensure the agent has it.
    """
    return Task(
        description=(
            "The document type has been validated. Now, analyze the full DOCUMENT TEXT and extract all important key-value pairs. "
            "Pay close attention to the schema to understand what to look for.\n"
            "--- DOCUMENT TEXT ---\n{invoice_text}"
        ),
        expected_output="A JSON object containing all extracted key-value pairs that loosely conforms to the 'InvoiceData' schema.",
        agent=agent,
        context=[context_task],
        # We make the output a dictionary to allow for dynamic keys found in the document
        output_json=InvoiceData 
    )

def create_review_task(agent: Agent, context_task: Task) -> Task:
    """
    Reviews the extracted data. We pass both the original text and the extractor's JSON output
    explicitly in the prompt to ensure the agent has all necessary information.
    """
    return Task(
        description=(
            "Your task is to critically review and validate the extracted data against the original text. "
            "The output from the previous agent is provided in the context.\n"
            "You MUST compare this extracted data to the full, original document text provided below.\n"
            "Correct any errors, add any missed information, and provide a summary of your actions.\n\n"
            "--- ORIGINAL DOCUMENT TEXT ---\n"
            "{invoice_text}"
        ),
        expected_output="A dictionary containing your 'review_summary' and the 'validated_data' dictionary.",
        agent=agent,
        context=[context_task]
    )

def create_consolidation_task(agent: Agent, validation_task: Task, review_task: Task) -> Task:
    """
    Assembles the final report. We pass the outputs of the validation and review tasks
    explicitly in the context to ensure the consolidator has all final data points.
    """
    return Task(
        description=(
            "Assemble the final report. You have been given the validated classification and the final reviewed data. "
            "Combine all this information into a single, comprehensive JSON object using the 'FinalReport' schema."
        ),
        expected_output="A final JSON report strictly adhering to the 'FinalReport' schema.",
        agent=agent,
        context=[validation_task, review_task], # Pass context from BOTH relevant tasks
        output_pydantic=FinalReport
    )