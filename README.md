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

## Usage

### Web Interface (Streamlit)

Run the Streamlit app:
```bash
streamlit run app.py
```

### Command Line

Run the CLI version:
```bash
python main.py
```

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy with `app.py` as entry point

### Docker

Build and run with Docker:
```bash
docker build -t job-app-copilot .
docker run -p 8501:8501 job-app-copilot
```

### Local Deployment

For local deployment with custom port:
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## Configuration

- `.streamlit/config.toml`: Streamlit configuration
- `config.py`: Application configuration
- `.env`: Environment variables