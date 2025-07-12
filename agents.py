
from crewai import Agent
from llm_wrappers import GeminiLLM

def create_dynamic_extractor_agent(llm: GeminiLLM) -> Agent:
    """Creates an agent that dynamically identifies and extracts key-value pairs."""
    return Agent(
        role='Dynamic Entity Extractor',
        goal=(
            "Identify and extract all significant key-value pairs from a given document text. "
            "The keys should be the labels found in the document (e.g., 'Loan Amount', 'Seller'), "
            "and the values should be their corresponding data."
        ),
        backstory=(
            'You are an expert financial analyst AI. You are not given a template. Instead, you intelligently scan documents, '
            'identify what information is important, and structure it as a dictionary of key-value pairs. '
            'You are looking for names, dates, addresses, financial figures, and important identifiers.'
        ),
        llm=llm,
        tools=[],
        verbose=True,
        allow_delegation=False
    )

def create_validator_agent(llm: GeminiLLM) -> Agent:
    """Creates a fact-checking agent that validates the dynamically extracted data."""
    return Agent(
        role='Data Fact-Checker and Validator',
        goal=(
            "Rigorously validate a dictionary of extracted key-value pairs against the original document text. "
            "Correct any inaccuracies, remove any hallucinated pairs, and add any critical information that was missed."
        ),
        backstory=(
            'You are a meticulous auditor AI. You receive raw text and a set of key-value pairs supposedly extracted from it. '
            'You do not trust the initial extraction. Your job is to fact-check every single item. '
            'For each key in the dictionary, you find that key in the original text and ensure the value is correct. '
            'Your final output is a clean, 100% factually-grounded dictionary of information.'
        ),
        llm=llm,
        tools=[],
        verbose=True,
        allow_delegation=False
    )