
# Try this App here at: 
https://automaticjobpilot.streamlit.app/

# Job Application Copilot

An AI-powered tool to help with job applications by generating tailored resume bullets and cover letters.

## Features

- AI agents for planning, writing, and verifying job application materials
- Streamlit web interface
- LangGraph workflow orchestration

## Project Structure

```
.
├── src/                    # Core application code
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── llm_client.py      # LLM client setup
│   ├── schemas.py         # Data schemas
│   ├── state.py           # Application state
│   └── workflow.py        # LangGraph workflow
├── agents/                 # AI agent implementations
│   ├── __init__.py
│   ├── cover_letter_agent.py
│   ├── planner.py
│   ├── verifier.py
│   └── writer.py
├── data/                   # Data files
│   ├── cover_letter.txt
│   └── tailored_bullets.txt
├── tests/                  # Test files
│   └── test.py
├── .streamlit/             # Streamlit configuration
│   └── config.toml
├── app.py                  # Streamlit application
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

