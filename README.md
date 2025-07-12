## Setup Instructions

Follow these steps to set up the project on your machine. 
( Tested on Ubuntu )

### Step 1: Install Tesseract OCR Engine

This is the most important prerequisite. Please follow the instructions for your operating system.


#### using ubuntu machine
```bash
sudo apt update
sudo apt install tesseract-ocr
```


### Step 2: Set Up the Project Environment

These steps are universal once Tesseract is installed.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Apex-AI-Company/Invoice-Extractor-Agent.git
    cd Invoice-Extractor-Agent
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # Create the environment
    python3 -m venv .virenv

    # Activate it 
    source .virenv/bin/activate
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a file named `.env` in the root of the project directory. Add your Google AI Studio API key to this file.
    ```ini
    # .env
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```

### Step 3: Run the Application

1.  **Place Your Document:** Add the document you want to process (e.g., `invoice.pdf` or `scan.png`) into the root directory of the project.

2.  **Update File Path:** Open the `main.py` file and update the `file_path` variable to point to your document.
    ```python
    # in main.py
    file_path = "your_document_name.pdf"
    ```

3.  **Execute the Script:** Run the main application from your terminal.
    ```bash
    python main.py
    ```

The system will process the document, and then print the final, structured summary report to the console.