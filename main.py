# main.py
import os
import sys
from dotenv import load_dotenv
from crewai import Crew, Process
from models import DynamicExtractionResult

# Import our custom modules
from llm_wrappers import GeminiLLM
from content_processing import extract_text_from_file
from agents import create_dynamic_extractor_agent, create_validator_agent
from tasks import create_dynamic_extraction_task, create_validation_task

def print_dynamic_summary(result: DynamicExtractionResult):
    """Takes the final Pydantic object and prints a dynamic report."""
    
    entities = result.extracted_entities
    
    # Organize keys into categories for cleaner printing (optional but nice)
    categories = {
        "Parties / People": ["seller", "buyer", "vendor", "lender", "borrower"],
        "Addresses": ["address"],
        "Dates": ["date"],
        "Financials": ["amount", "total", "subtotal", "tax", "price", "rate", "interest"],
        "Identifiers": ["number", "id", "mic"]
    }

    # Group entities by category
    grouped_entities = {cat: {} for cat in categories}
    other_entities = {}

    for key, value in entities.items():
        if not value: continue # Skip empty values
        
        found = False
        for cat, keywords in categories.items():
            if any(keyword in key.lower() for keyword in keywords):
                grouped_entities[cat][key] = value
                found = True
                break
        if not found:
            other_entities[key] = value
            
    # Print the report
    for cat, items in grouped_entities.items():
        if items:
            print(f"{cat}:")
            for key, value in items.items():
                # Clean up the key for printing and format the value
                display_key = key.replace("_", " ").title()
                if isinstance(value, float):
                    display_value = f"${value:,.2f}"
                else:
                    display_value = str(value).replace('\n', ', ')
                print(f"  - {display_key}: {display_value}")
            print() # Add a newline for spacing

    if other_entities:
        print("Other Information:")
        for key, value in other_entities.items():
            display_key = key.replace("_", " ").title()
            display_value = str(value).replace('\n', ', ')
            print(f"  - {display_key}: {display_value}")
        print()
        
    print("--- Reviewer Comments ---")
    print(f"{result.review_summary}")


# --- SETUP & EXECUTION (This part remains mostly the same) ---

load_dotenv()
file_path = "image.jpg"
# file_path = "Acord_PDF.pdf"
# file_path = "Invoice_sample1.png"
if not os.path.exists(file_path):
    sys.exit(f"[FATAL ERROR] File not found: {file_path}")

print(f"Processing document: {file_path}")
invoice_text = extract_text_from_file(file_path)
if "Error:" in invoice_text:
    sys.exit(f"[FATAL ERROR] {invoice_text}")

llm = GeminiLLM()
print(f"LLM Initialized: {llm.model}")

# Create the new dynamic agents and tasks
extractor_agent = create_dynamic_extractor_agent(llm)
validator_agent = create_validator_agent(llm)
print("Agents are defined.")

extraction_task = create_dynamic_extraction_task(extractor_agent)
validation_task = create_validation_task(validator_agent, context_task=extraction_task)
print("Tasks are defined.")

extraction_crew = Crew(
    agents=[extractor_agent, validator_agent],
    tasks=[extraction_task, validation_task],
    process=Process.sequential,
    verbose=True
)

crew_inputs = {'invoice_text': invoice_text}

print("\nKicking off the Entity Extraction Crew...")
result = extraction_crew.kickoff(inputs=crew_inputs)

print("\n\n Crew execution finished!")
print("="*50)
print("          Entity  SUMMARY")
print("="*50)

final_pydantic_object = result.pydantic if hasattr(result, 'pydantic') else None

if isinstance(final_pydantic_object, DynamicExtractionResult):
    print_dynamic_summary(final_pydantic_object)
else:
    print("Could not parse the final structured output. Here is the raw result:")
    print(result)

print("="*50)