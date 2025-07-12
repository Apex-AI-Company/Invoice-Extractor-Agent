import os
import sys
from dotenv import load_dotenv
from crewai import Crew, Process

from llm_wrappers import GeminiLLM
from content_processing import extract_text_from_file
from agents import (
    create_classifier_agent,
    create_validator_agent,
    create_extraction_agent,
    create_reviewer_agent,
    create_consolidator_agent
)
from tasks import (
    create_classification_task,
    create_validation_task,
    create_extraction_task,
    create_review_task,
    create_consolidation_task
)

# --- SETUP & PRE-PROCESSING ---
load_dotenv()
file_path = "Acord_PDF.pdf"
if not os.path.exists(file_path):
    sys.exit(f"[FATAL ERROR] File not found: {file_path}")

print(f"Processing document: {file_path}") # extract text from the file
invoice_text = extract_text_from_file(file_path)
if "Error:" in invoice_text:
    sys.exit(f"[FATAL ERROR] {invoice_text}")

# --- INITIALIZE THE CREW ---
llm = GeminiLLM()
print(f"LLM Initialized: {llm.model}")

# Create the full agent workforce
classifier = create_classifier_agent(llm)
validator = create_validator_agent(llm)
extractor = create_extraction_agent(llm)
reviewer = create_reviewer_agent(llm)
consolidator = create_consolidator_agent(llm)
print("All agents are defined.")

# Create the full task pipeline
task1 = create_classification_task(classifier)
task2 = create_validation_task(validator, context_task=task1)
task3 = create_extraction_task(extractor, context_task=task2)
task4 = create_review_task(reviewer, context_task=task3)
task5 = create_consolidation_task(consolidator, validation_task=task2, review_task=task4)
print("All tasks are defined and linked.")

# Assemble the final crew
crew = Crew(
    agents=[classifier, validator, extractor, reviewer, consolidator],
    tasks=[task1, task2, task3, task4, task5],
    process=Process.sequential,
    verbose=True
)

# --- EXECUTE THE CREW ---
crew_inputs = {'invoice_text': invoice_text}
print("\nKicking off the Full Document Processing Crew...")
result = crew.kickoff(inputs=crew_inputs)

# --- PRINT THE FINAL,  RESULT ---
print("\n\nCrew execution finished!")
print("="*50)
print("           REPORT ")
print("="*50)

# The result is now the 'FinalReport' Pydantic object, which is already clean.
if hasattr(result, 'pydantic') and result.pydantic:
    # Use .model_dump_json for a clean, indented JSON string output
    print(result.pydantic.model_dump_json(indent=2))
else:
    print("Could not parse the final structured output. Here is the raw result:")
    print(result)

print("="*50)