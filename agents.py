from crewai import Agent
from llm_wrappers import GeminiLLM

def create_classifier_agent(llm: GeminiLLM) -> Agent:
    return Agent(
        role='Document Classification Specialist',
        goal="Accurately classify the document based on its content from a predefined list of types: ['Invoice', 'Loan Disclosure', 'Resume', 'Unknown'].",
        backstory="You are an AI expert trained to identify document types by analyzing their text for keywords and structure.",
        llm=llm, tools=[], verbose=True
    )

def create_validator_agent(llm: GeminiLLM) -> Agent:
    return Agent(
        role='Classification Validator',
        goal="Cross-verify the initial document classification. Your job is to confirm the classification is correct or to change it if it's wrong.",
        backstory="You are a meticulous auditor. You don't trust the first classification. You validate it by checking for expected patterns (e.g., an invoice must have an invoice number).",
        llm=llm, tools=[], verbose=True
    )

def create_extraction_agent(llm: GeminiLLM) -> Agent:
    return Agent(
        role='Dynamic Entity Extractor',
        goal="Dynamically identify and extract all significant key-value pairs from the document based on its validated type.",
        backstory="You are an expert financial analyst AI. You intelligently scan documents and structure all important information into a comprehensive dictionary.",
        llm=llm, tools=[], verbose=True
    )

def create_reviewer_agent(llm: GeminiLLM) -> Agent:
    return Agent(
        role='Data Fact-Checker and Auditor',
        goal="Rigorously validate a dictionary of extracted key-value pairs against the original document text, correcting any errors and adding any missed information.",
        backstory="You are the last line of defense for data accuracy. You do not trust the initial extraction and your value comes from finding errors and omissions.",
        llm=llm, tools=[], verbose=True
    )

def create_consolidator_agent(llm: GeminiLLM) -> Agent:
    return Agent(
        role='Final Report Generator',
        goal="Compile all the information from the previous steps (classification, validation, extraction, and review) into a single, final, comprehensive report.",
        backstory="You are the secretary of this AI crew. You take all the outputs from your colleagues and assemble them into a clean, well-structured final JSON object for the user.",
        llm=llm, tools=[], verbose=True
    )